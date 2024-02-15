using static NakaScript.Components.Constants;

namespace NakaScript.Components
{
    internal class DebugUtils
    {
        public static void DebugMessage(string message)
        {
            #pragma warning disable CS0162 // Unreachable code detected
            if (!DEBUG_MESSAGES) { return; }

            Console.WriteLine("[DEBUG] " + message);
        }
    }
}
