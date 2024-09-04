using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEditor;

public class AssetGenerator : EditorWindow
{
    [MenuItem("Window/Asset Generator")]
    public static void ShowWindow()
    {
        EditorWindow.GetWindow(typeof(AssetGenerator));
    }
}