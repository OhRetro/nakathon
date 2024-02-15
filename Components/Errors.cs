namespace NakaScript.Components
{
    internal class Errors
    {
        public class Error(Position posStart, Position posEnd, string errorName, string details)
        {
            public Position posStart = posStart;
            public Position posEnd = posEnd;

            public string errorName = errorName;
            public string details = details;

            public override string ToString()
            {
                string fullError = "";
                fullError += $"{errorName}: {details}\n";
                fullError += $"File: {posStart.filename}, line {posStart.line + 1}\n\n";
              
                return fullError;
            }

            public void ShowError() => Console.WriteLine(this);
        }

        public class IllegalCharError(Position posStart, Position posEnd, string details) : Error(posStart, posEnd, "Illegal Character", details) { }
        public class InvalidSyntaxError(Position posStart, Position posEnd, string details) : Error(posStart, posEnd, "Invalid Syntax", details) { }
    }

}
