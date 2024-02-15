using System.Reflection;
using static NakaScript.Components.Nodes;

namespace NakaScript.Components
{
    internal class Interpreter
    {
        public object? Visit(dynamic node)
        {
            string methodName = $"Visit{node.name}";
            MethodInfo theMethod = GetType().GetMethod(methodName);
            return theMethod.Invoke(this, [node]);
        }

        public void VisitNumberNode(Node node)
        {
            Console.WriteLine("Found Number");
        }
        public void VisitBineryOperationNode(Node node)
        {
            Console.WriteLine("Found BinOp");
        }
        public void VisitUnaryOperationNode(Node node)
        {
            Console.WriteLine("Found UnaOp");
        }
        public void NoVisitMethod() 
        {
            throw new Exception("No Visit Method Defined");
        }
    }
}
