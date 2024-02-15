using static NakaScript.Components.Constants;
using static NakaScript.Components.Errors;
using static NakaScript.Components.Tokens;

namespace NakaScript.Components
{
    internal class Lexer
    {
        public string filename;
        public string text;

        private Position pos;
        private char currentChar;

        public Lexer(string filename, string text)
        {
            this.filename = filename;
            this.text = text;

            pos = new(-1, 0, -1, filename, text);
            currentChar = NULL_CHAR;

            Advance();
        }

        public void Advance()
        {
            pos = pos.Advance(currentChar);
            if (pos.index < text.Length)
            {
                currentChar = text[pos.index];
            }
            else
            {
                currentChar = NULL_CHAR;
            }
        }

        public (Token[], Error) MakeTokens()
        {
            var tokens = new List<Token>();

            while (currentChar != NULL_CHAR)
            {
                if (char.IsWhiteSpace(currentChar))
                {
                    Advance();
                }
                else if (DIGITS.Contains(currentChar))
                {
                    tokens.Add(MakeNumber());
                }
                else if (currentChar == '+')
                {
                    tokens.Add(new Token(TokenType.PLUS, null, pos));
                    Advance();
                }
                else if (currentChar == '-')
                {
                    tokens.Add(new Token(TokenType.MINUS, null, pos));
                    Advance();
                }
                else if (currentChar == '*')
                {
                    tokens.Add(new Token(TokenType.MUL, null, pos));
                    Advance();
                }
                else if (currentChar == '/')
                {
                    tokens.Add(new Token(TokenType.DIV, null, pos));
                    Advance();
                }
                else if (currentChar == '(')
                {
                    tokens.Add(new Token(TokenType.LPAREN, null, pos));
                    Advance();
                }
                else if (currentChar == ')')
                {
                    tokens.Add(new Token(TokenType.RPAREN, null, pos));
                    Advance();
                }
                else
                {
                    var illegalPosStart = pos.Copy();
                    var illegalChar = currentChar;
                    Advance();
                    return ([], new IllegalCharError(illegalPosStart, pos, illegalChar.ToString()));
                }
            }

            tokens.Add(new Token(TokenType.EOF, null, pos));

            return (tokens.ToArray(), NO_ERROR);
        }

        public Token MakeNumber()
        {
            var numStr = "";
            var dotCount = 0;
            var posStart = pos.Copy();

            while (currentChar != NULL_CHAR && DIGITS.Concat(".").Contains(currentChar))
            {
                if (currentChar == '.')
                {
                    if (dotCount == 1) { break; }
                    dotCount++;
                    numStr += ".";
                }
                else
                {
                    numStr += currentChar.ToString();
                }
                Advance();
            }

            if (dotCount == 0) { return new Token(TokenType.INT, int.Parse(numStr), posStart, pos); }
            else { return new Token(TokenType.FLOAT, float.Parse(numStr), posStart, pos); }
        }
    }
}
