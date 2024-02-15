namespace NakaScript.Components
{
    internal class Tokens
    {
        public static void ShowTokens(Token[] tokens) => Console.WriteLine("[" + string.Join<Token>(", ", tokens) + "]");

        public enum TokenType
        {
            NONE,
            INT,
            FLOAT,
            PLUS,
            MINUS,
            MUL,
            DIV,
            LPAREN,
            RPAREN,
            EOF
        }

        public class Token
        {
            public TokenType type;
            public dynamic? value;
            public Position? posStart;
            public Position? posEnd;

            public Token(TokenType type, dynamic? value = null, Position? posStart = null, Position? posEnd = null) {
                this.type = type;
                this.value = value;

                if (posStart != null) 
                {
                    this.posStart = posStart.Copy();
                    this.posEnd = posStart.Copy();
                    this.posEnd.Advance();
                }

                if (posEnd != null)
                {
                    this.posEnd = posEnd.Copy();
                }
            }

            public override string ToString()
            {
                if (value != null)
                {
                    return string.Format("{0}:{1}", type, value);
                }
                return type.ToString();
            }
        }
    }
}
