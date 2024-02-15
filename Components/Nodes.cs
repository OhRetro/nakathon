using static NakaScript.Components.Tokens;
using static NakaScript.Components.DebugUtils;

namespace NakaScript.Components
{
    internal class Nodes
    {
        public enum NodeType
        {
            None,
            Generic,
            Dynamic,
            Number,
            BineryOperation,
            UnaryOperation
        }

        public class Node
        {
            public NodeType type;
            public Token token;
            public string name;

            public Node(NodeType type, Token token)
            {
                this.type = type;
                this.token = token; 
                name = GetType().Name;

                DebugMessage($"Created {name} {this}");
            }

            public override string ToString()
            {
                return $"[{type}:{token}]";
            }
        }

        public class NumberNode(Token token) : Node(NodeType.Number, token) { }
        public class BineryOperationNode(Token token, Node leftNode, Node rightNode) : Node(NodeType.BineryOperation, token) 
        {
            public Token opToken = token;
            public Node leftNode = leftNode;
            public Node rightNode = rightNode;

            public override string ToString()
            {
                return $"({leftNode}, {opToken.type}:{opToken}, {rightNode})";
            }
        }

        public class UnaryOperationNode(Token token, Node node) : Node(NodeType.UnaryOperation, token) 
        {
            public Token opToken = token;
            public Node node = node;

            public override string ToString()
            {
                return $"({opToken}, {node})";
            }
        }
    }
}
