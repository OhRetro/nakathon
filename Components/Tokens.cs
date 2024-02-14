namespace NakaScript
{
    public enum TokenType
    {
        INT,
        FLOAT,
        PLUS,
        MINUS,
        MUL,
        DIV,
        LPAREN,
        RPAREN
    }

    public class Token(TokenType type, dynamic? value = null)
    {
        public TokenType type = type;
        public dynamic value = value;


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
