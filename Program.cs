﻿using static NakaScript.Components.Errors;
using static NakaScript.Components.Tokens;
using static NakaScript.Components.Constants;
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

                if (error != NO_ERROR)
                {
                    error.ShowError();
                }
                else
                {
                    Console.WriteLine(tokens);
                }
            }

        }
      
        static (dynamic, Error) Run(string filename, string text)
        {
            Lexer lexer = new(filename, text);

            (Token[] tokens, Error error) = lexer.MakeTokens();

            if (error != NO_ERROR)
            {
                return (tokens, error);
            }

            Parser parser = new(tokens);

            var ast = parser.Parse();

            if (ast.error != NO_ERROR)
            {
                return (tokens, ast.error);
            }

            Interpreter interpreter = new Interpreter();
            interpreter.Visit(ast.node);

            return (ast.node, ast.error);
        }
    }
}