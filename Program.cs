namespace NakaScript
{
    internal class Program
    {
        static void Main(string[] args)
        {
            Console.Write(">");
            var text = Console.ReadLine();
            (List<Token> result, dynamic? error) returned = Run(text); 

            if (returned.error != null) {
                Console.WriteLine(returned.error.ToString());
            } 
            else
            {
                Console.WriteLine(returned.result.ToString());
            }
        }

        static (List<Token>, dynamic?) Run(string text)
        {
            var lexer = new Lexer(text);
            
            return lexer.MakeTokens();
        }
    }
}