using static NakaScript.Components.Errors;
using static NakaScript.Components.Tokens;
using static NakaScript.Components.Nodes;

namespace NakaScript.Components
{
    internal class Constants
    {
        public const bool DEBUG_MESSAGES = true;

        public static readonly string DIGITS = "0123456789";

        public const char NULL_CHAR = '\0';
        public const char NEW_LINE = '\n';

        public static readonly Token NO_TOKEN = new(TokenType.NONE);
        public static readonly Position NO_POSITION = new(0, 0, 0, "", "");
        public static readonly Error NO_ERROR = new(NO_POSITION, NO_POSITION, "No Error", "This is meant to replace the need to return 'null' and setting the return type to 'dynamic?' in a function.");
        public static readonly Node NO_NODE = new(NodeType.None, NO_TOKEN);
    }
}
