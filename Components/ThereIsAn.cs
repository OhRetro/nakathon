using static NakaScript.Components.Constants;
using static NakaScript.Components.Errors;
using static NakaScript.Components.Nodes;
using static NakaScript.Components.Tokens;

namespace NakaScript.Components
{
    internal class ThereIsAn
    {
        public static bool ThereIsAnToken(Token token) => token != NO_TOKEN;
        public static bool ThereIsAnPosition(Position position) => position != NO_POSITION;
        public static bool ThereIsAnError(Error error) => error != NO_ERROR;
        public static bool ThereIsAnNode(Node node) => node != NO_NODE;
    }
}
