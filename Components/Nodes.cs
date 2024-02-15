using static NakaScript.Components.Tokens;

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

        public class Node(NodeType type, Token token)
        {
            public NodeType type = type;
            public Token token = token;

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
                return $"({leftNode}, {opToken}, {rightNode})";
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
