using static NakaScript.Components.Constants;

namespace NakaScript.Components
{
    internal class Position(int index, int line, int column, string filename, string filetext)
    {
        public int index = index;
        public int line = line;
        public int column = column;

        public string filename = filename;
        public string filetext = filetext;

        public Position Advance(char currentChar = NULL_CHAR)
        {
            index++;
            column++;

            if (currentChar == NEW_LINE)
            {
                line++;
                column = 0;
            }

            return this;
        }

        public Position Copy()
        {
            return new Position(index, line, column, filename, filetext);
        }
    }
}
