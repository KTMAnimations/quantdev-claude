export function validatePineSyntax(code: string): {
  is_valid: boolean;
  errors: string[];
  warnings: string[];
} {
  const errors: string[] = [];
  const warnings: string[] = [];

  if (!code.includes("//@version=5") && !code.includes("//@version=4")) {
    errors.push("Missing version declaration (//@version=5)");
  }

  if (!code.includes("indicator(") && !code.includes("strategy(")) {
    errors.push("Missing indicator() or strategy() declaration");
  }

  if ((code.match(/\(/g) ?? []).length !== (code.match(/\)/g) ?? []).length) {
    errors.push("Mismatched parentheses");
  }

  if ((code.match(/\[/g) ?? []).length !== (code.match(/]/g) ?? []).length) {
    errors.push("Mismatched brackets");
  }

  const varIdx = code.indexOf("var ");
  if (varIdx !== -1) {
    const next = code.slice(varIdx, varIdx + 50);
    if (!next.includes("=")) {
      warnings.push("'var' keyword may be incorrectly used");
    }
  }

  return { is_valid: errors.length === 0, errors, warnings };
}

