using static NakaScript.Components.Errors;
using static NakaScript.Components.Tokens;
using static NakaScript.Components.ThereIsAn;
using static NakaScript.Components.Constants;
using static NakaScript.Components.DebugUtils;
using NakaScript.Components;

namespace NakaScript
{
    internal class Program
    {
        static void Main()
        {
            while (true)
            {
                Console.Write("ns shell > ");
                var text = Console.ReadLine();
                (dynamic tokens, Error error) = Run("shell", text);

                if (ThereIsAnError(error))
                {
                    DebugMessage("Showing Error");
                    error.ShowError();
                }
                else
                {
                    DebugMessage("Showing Results");
                    Console.WriteLine(tokens);
                }
            }

        }
      
        static (dynamic, Error) Run(string filename, string text)
        {
            Lexer lexer = new(filename, text);

            (Token[] tokens, Error error) = lexer.MakeTokens();

            if (ThereIsAnError(error))
            {
                return (tokens, error);
            }

            Parser parser = new(tokens);

            var ast = parser.Parse();

            if (ThereIsAnError(error))
            {
                return (tokens, ast.error);
            }

            Interpreter interpreter = new();
            interpreter.Visit(ast.node);

            return (ast.node, ast.error);
        }
    }
}