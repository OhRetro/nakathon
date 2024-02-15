﻿using static NakaScript.Components.Tokens;
using static NakaScript.Components.Nodes;
using static NakaScript.Components.Constants;
using static NakaScript.Components.Errors;

namespace NakaScript.Components
{
    internal class ParseResult
    {
        public Error error = NO_ERROR;
        public Node? node;

        public override string ToString()
        {
            return string.Format("{0}", node);
        }

        public dynamic? Register(dynamic? result) 
        {
            if (result is ParseResult)
            {
                if (result.error != NO_ERROR)
                {
                    this.error = result.error;
                    return result.node;
                }
            }

            return result;
        }

        public ParseResult Success(Node node)
        {
            this.node = node;
            return this;
        }
        public ParseResult Failure(Error error)
        {
            this.error = error;
            return this;
        }
    }
    internal class Parser
    {
        Token[] tokens;
        Token currentToken = NO_TOKEN;
        int tokenIndex = -1;

        public Parser(Token[] tokens)
        {
            this.tokens = tokens;
            Advance();
        }

        public dynamic Parse()
        {
            var result = Expr();

            if (result.error == NO_ERROR && currentToken.type != TokenType.EOF)
            {
                return result.Failure(new InvalidSyntaxError(
                        currentToken.posStart, currentToken.posEnd,
                        "Expected '+', '-', '*' or '/'."
                    ));
            }

            return result;
        }

        public Token Advance()
        {
            tokenIndex++;

            if (tokenIndex < tokens.Length)
            {
                currentToken = tokens[tokenIndex];
            }

            return currentToken;
        }

        public dynamic? Factor() { 
            var result = new ParseResult();
            var token = currentToken;

            TokenType[] sign = [TokenType.PLUS, TokenType.MINUS];
            TokenType[] operations = [TokenType.INT, TokenType.FLOAT];

            if (sign.Contains(token.type))
            {
                result.Register(Advance());
                var factor = result.Register(Factor());

                if (result.error != NO_ERROR)
                {
                    return result;
                }

                return result.Success(new UnaryOperationNode(token, factor));
            }
            else if (operations.Contains(token.type))
            {
                result.Register(Advance());
                return result.Success(new NumberNode(token));
            }
            else if (token.type == TokenType.LPAREN)
            {
                result.Register(Advance());
                var expr = result.Register(Expr());

                if (result.error != NO_ERROR)
                {
                    return result;
                }

                if (currentToken.type == TokenType.RPAREN)
                {
                    result.Register(Advance());
                    return result.Success(expr);
                }
                else
                {
                    return result.Failure(new InvalidSyntaxError(
                        token.posStart, token.posEnd,
                        "Expected ')'"
                    ));
                }
            }

            return result.Failure(new InvalidSyntaxError(
                    token.posStart, token.posEnd,
                    "Expected int or float."
                ));
        }
        public dynamic Term() 
        {
            return BineryOperation(Factor, [TokenType.MUL, TokenType.DIV]);
        }
        public dynamic Expr() 
        {
            return BineryOperation(Term, [TokenType.PLUS, TokenType.MINUS]);
        }

        public dynamic BineryOperation(Func<dynamic> function, TokenType[] operations)
        {
            var result = new ParseResult();
            dynamic? leftNode = result.Register(function());

            if (result.error != NO_ERROR)
            {
                return result;
            }
            
            while (operations.Contains(currentToken.type))
            {
                var opToken = currentToken;
                result.Register(Advance());
                var rightNode = result.Register(function());
                if (result.error != NO_ERROR)
                {
                    return result;
                }

                leftNode = new BineryOperationNode(opToken, leftNode, rightNode);
            }
            Console.WriteLine("a");
            return result.Success(leftNode);
        }
    }
}
