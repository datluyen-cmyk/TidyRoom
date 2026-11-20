using System;
using System.IO;
using System.Collections;
using UnityEngine;
using UnityEngine.Networking;

namespace TidyRoom
{
    // Android StreamingAssets live inside the APK, so copy requested files through UnityWebRequest.
    public static class TidyAssetCache
    {
        public static bool InAndroidPlayer=>Application.platform==RuntimePlatform.Android;
        public static string Root=>InAndroidPlayer?Path.Combine(Application.persistentDataPath,"TidyRoom",Application.buildGUID):Path.Combine(Application.streamingAssetsPath,"TidyRoom");
        public static IEnumerator Fetch(string relative,Action<string> onError)
        {
            string destination=Path.Combine(Root,relative);
            if(File.Exists(destination))yield break;
            string url=Application.streamingAssetsPath.TrimEnd('/')+"/TidyRoom/"+relative.Replace('\\','/');
            using(var request=UnityWebRequest.Get(url))
            {
                request.timeout=30;yield return request.SendWebRequest();
                if(request.result!=UnityWebRequest.Result.Success){onError(relative+": "+request.error);yield break;}
                try{Directory.CreateDirectory(Path.GetDirectoryName(destination));File.WriteAllBytes(destination,request.downloadHandler.data);}
                catch(Exception e){onError(e.Message);}
            }
        }
    }
}
