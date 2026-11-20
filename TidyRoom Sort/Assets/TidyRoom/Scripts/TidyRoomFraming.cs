using System.Linq;
using UnityEngine;

namespace TidyRoom
{
    // Coordinates shared with the HUD shields: header ends at 550, footer starts at -810.
    public sealed class TidyRoomFraming
    {
        public static readonly Rect PlayArea=Rect.MinMaxRect(-540,-810,540,550);
        public readonly Rect Content,Bounds;
        public readonly float Scale;

        public TidyRoomFraming(LevelData level,Vector2 backgroundSize)
        {
            var items=level.content.Select(i=>i.Bounds()).ToArray();
            Content=Rect.MinMaxRect(items.Min(b=>b.xMin)-25,items.Min(b=>b.yMin)-25,
                items.Max(b=>b.xMax)+25,items.Max(b=>b.yMax)+25);
            Bounds=Rect.MinMaxRect(Mathf.Min(-backgroundSize.x/2,Content.xMin),Mathf.Min(-backgroundSize.y/2,Content.yMin),
                Mathf.Max(backgroundSize.x/2,Content.xMax),Mathf.Max(backgroundSize.y/2,Content.yMax));
            float allItems=Mathf.Min(1040/Content.width,1300/Content.height);
            // Keep room art behind the overlay HUD as well as the playable area.
            float cover=Mathf.Max(1080/backgroundSize.x,1920/backgroundSize.y);
            // Wide rooms are explored by dragging instead of shrinking everything or stretching art.
            Scale=Mathf.Max(allItems,cover);
        }

        public Vector2 Clamp(Vector2 position,float scale)
        {
            return new Vector2(ClampAxis(position.x,Bounds.xMin,Bounds.xMax,PlayArea.xMin,PlayArea.xMax,scale),
                ClampAxis(position.y,Bounds.yMin,Bounds.yMax,PlayArea.yMin,PlayArea.yMax,scale));
        }

        static float ClampAxis(float position,float min,float max,float viewMin,float viewMax,float scale)
        {
            if((max-min)*scale<=viewMax-viewMin)return (viewMin+viewMax-(min+max)*scale)/2;
            return Mathf.Clamp(position,viewMax-max*scale,viewMin-min*scale);
        }
    }
}
