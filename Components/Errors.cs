namespace NakaScript
{
    public class Error(string errorName, string details)
    {
        public string errorName = errorName;
        public string details = details;

        public override string ToString()
        {
            return string.Format("{0}: {1}", errorName, details);
        }
    }
    public class IllegalCharError(string details) : Error("Illegal Character", details)
    {
    }
}
