using static NakaScript.Constants;

namespace NakaScript
{
    internal class Lexer(string text)
    {
        public string text = text;
        private int pos = -1;
        private char currentChar = '\0';

        public void Advance()
        {
            pos++;
            if (pos < text.Length)
            {
                currentChar = text[pos];
            }
            else
            {
                currentChar = '\0';
            }

        }

        public (List<Token>, dynamic?) MakeTokens()
        {
            var tokens = new List<Token>();

            while (currentChar != '\0')
            {
                if (char.IsWhiteSpace(currentChar))
                {
                    Advance();
                }
                else if (DIGITS.Contains(currentChar))
                {
                    tokens.Add(MakeNumber());
                    Advance();
                }
                else if (currentChar == '+')
                {
                    tokens.Add(new Token(TokenType.PLUS));
                    Advance();
                }
                else if (currentChar == '-')
                {
                    tokens.Add(new Token(TokenType.MINUS));
                    Advance();
                }
                else if (currentChar == '*')
                {
                    tokens.Add(new Token(TokenType.MUL));
                    Advance();
                }
                else if (currentChar == '/')
                {
                    tokens.Add(new Token(TokenType.DIV));
                    Advance();
                }
                else if (currentChar == '(')
                {
                    tokens.Add(new Token(TokenType.LPAREN));
                    Advance();
                }
                else if (currentChar == ')')
                {
                    tokens.Add(new Token(TokenType.RPAREN));
                    Advance();
                }
                else
                {
                    var illegalChar = currentChar;
                    Advance();
                    return ([], new IllegalCharError(illegalChar.ToString()));
                }
            }

            return (tokens, null);
        }

        public Token MakeNumber()
        {
            var numStr = "";
            var dotCount = 0;

            while (currentChar != '\0' && string.Concat(DIGITS, ".").Contains(currentChar))
            {
                if (currentChar == '.')
                {
                    if (dotCount == 1) { break; }
                    dotCount++;
                    numStr += ".";
                }
                else
                {
                    numStr += currentChar;
                }
                Advance();
            }

            if (dotCount == 0)
            {
                return new Token(TokenType.INT, int.Parse(numStr));
            }
            else
            {
                return new Token(TokenType.FLOAT, float.Parse(numStr));
            }
        }
    }
}
