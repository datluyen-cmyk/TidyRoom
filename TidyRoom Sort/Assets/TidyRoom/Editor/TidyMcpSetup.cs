using UnityEditor;
using UnityEngine;
using MCPForUnity.Editor.Services;
using MCPForUnity.Editor.Services.Transport;

[InitializeOnLoad]
public static class TidyMcpSetup
{
    static TidyMcpSetup() { EditorApplication.delayCall += Connect; }
    [MenuItem("Tidy Room/Connect Unity MCP")]
    public static async void Connect()
    {
        if (EditorApplication.isCompiling) return;
        EditorPrefs.SetBool("MCPForUnity.UseHttpTransport", true);
        EditorPrefs.SetString("MCPForUnity.HttpUrl", "http://127.0.0.1:8080");
        try { await MCPServiceLocator.TransportManager.StartAsync(TransportMode.Http); }
        catch (System.Exception e) { Debug.LogWarning("Tidy MCP: " + e.Message); }
    }
}
