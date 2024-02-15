
export enum TokenType {
	// Literal Types
	Number,
	Identifier,

	// Keywords
	Let,

	// Grouping * Operators
	BinaryOperator,
	Equals,
	OpenParen,
	CloseParen,
}


const KEYWORDS: Record<string, TokenType> = {
	let: TokenType.Let,
};

export interface Token {
	value: string;
	type: TokenType;
}

function token(value = "", type: TokenType): Token {
	return { value, type };
}


function isalpha(src: string) {
	return src.toUpperCase() != src.toLowerCase();
}


function isskippable(str: string) {
	return str == " " || str == "\n" || str == "\t";
}


function isint(str: string) {
	const c = str.charCodeAt(0);
	const bounds = ["0".charCodeAt(0), "9".charCodeAt(0)];
	return c >= bounds[0] && c <= bounds[1];
}

export function tokenize(sourceCode: string): Token[] {
	const tokens = new Array<Token>();
	const src = sourceCode.split("");

	// produce tokens until the EOF is reached.
	while (src.length > 0) {
		// BEGIN PARSING ONE CHARACTER TOKENS
		if (src[0] == "(") {
			tokens.push(token(src.shift(), TokenType.OpenParen));
		} else if (src[0] == ")") {
			tokens.push(token(src.shift(), TokenType.CloseParen));
		} // HANDLE BINARY OPERATORS
		else if (src[0] == "+" || src[0] == "-" || src[0] == "*" || src[0] == "/") {
			tokens.push(token(src.shift(), TokenType.BinaryOperator));
		} // Handle Conditional & Assignment Tokens
		else if (src[0] == "=") {
			tokens.push(token(src.shift(), TokenType.Equals));
		} // HANDLE MULTICHARACTER KEYWORDS, TOKENS, IDENTIFIERS ETC...
		else {
			// Handle numeric literals -> Integers
			if (isint(src[0])) {
				let num = "";
				while (src.length > 0 && isint(src[0])) {
					num += src.shift();
				}

				// append new numeric token.
				tokens.push(token(num, TokenType.Number));
			} // Handle Identifier & Keyword Tokens.
			else if (isalpha(src[0])) {
				let ident = "";
				while (src.length > 0 && isalpha(src[0])) {
					ident += src.shift();
				}

				const reserved = KEYWORDS[ident];

				if (reserved) {
					tokens.push(token(ident, reserved));
				} else {
					tokens.push(token(ident, TokenType.Identifier));
				}
			} else if (isskippable(src[0])) {
				src.shift();
            }
			else {
				console.error(
					"Unreconized character found in source: ",
					src[0].charCodeAt(0),
					src[0]
				);
				return [];
			}
		}
	}

	return tokens;
}