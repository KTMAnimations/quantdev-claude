"use client";

import { useRef, useState } from "react";
import Editor, { OnMount } from "@monaco-editor/react";
import { editor } from "monaco-editor";
import { Button } from "@/components/ui/button";
import { Copy, Download, Wand2, AlertCircle, CheckCircle } from "lucide-react";

// Pine Script language definition
const PINE_LANGUAGE_DEF = {
  keywords: [
    "if", "else", "for", "to", "while", "switch", "case", "default",
    "break", "continue", "return", "import", "export", "type", "enum",
    "var", "varip", "const", "input", "series", "simple",
    "true", "false", "na", "bar_index", "last_bar_index",
    "strategy", "indicator", "library"
  ],
  typeKeywords: [
    "int", "float", "bool", "string", "color", "line", "label", "box",
    "table", "array", "matrix", "map"
  ],
  builtins: [
    "ta", "math", "str", "color", "array", "matrix", "map", "chart",
    "request", "ticker", "syminfo", "timeframe", "session", "strategy"
  ],
  operators: [
    "=", ">", "<", "!", "~", "?", ":", "==", "<=", ">=", "!=",
    "and", "or", "not", "+", "-", "*", "/", "%", "+=", "-=", "*=", "/="
  ]
};

interface PineScriptEditorProps {
  value: string;
  onChange: (value: string) => void;
  onGenerate?: (description: string) => Promise<void>;
  isGenerating?: boolean;
  validationErrors?: string[];
}

export function PineScriptEditor({
  value,
  onChange,
  onGenerate,
  isGenerating,
  validationErrors = []
}: PineScriptEditorProps) {
  const editorRef = useRef<editor.IStandaloneCodeEditor | null>(null);
  const [description, setDescription] = useState("");

  const handleEditorDidMount: OnMount = (editorInstance, monaco) => {
    editorRef.current = editorInstance;

    // Register Pine Script language
    monaco.languages.register({ id: "pinescript" });

    // Set tokenizer
    monaco.languages.setMonarchTokensProvider("pinescript", {
      keywords: PINE_LANGUAGE_DEF.keywords,
      typeKeywords: PINE_LANGUAGE_DEF.typeKeywords,
      operators: PINE_LANGUAGE_DEF.operators,

      tokenizer: {
        root: [
          [/\/\/.*$/, "comment"],
          [/\/\*/, "comment", "@comment"],
          [/"([^"\\]|\\.)*$/, "string.invalid"],
          [/"/, "string", "@string"],
          [/'[^']*'/, "string"],
          [/\d+\.?\d*/, "number"],
          [/#[0-9a-fA-F]{6,8}/, "color"],
          [
            /[a-zA-Z_]\w*/,
            {
              cases: {
                "@keywords": "keyword",
                "@typeKeywords": "type",
                "@default": "identifier"
              }
            }
          ],
          [/[{}()\[\]]/, "@brackets"],
          [/[<>](?!@operators)/, "@brackets"],
        ],
        comment: [
          [/[^\/*]+/, "comment"],
          [/\*\//, "comment", "@pop"],
          [/[\/*]/, "comment"]
        ],
        string: [
          [/[^\\"]+/, "string"],
          [/\\./, "string.escape"],
          [/"/, "string", "@pop"]
        ]
      }
    });

    // Define dark theme for Pine Script
    monaco.editor.defineTheme("pine-dark", {
      base: "vs-dark",
      inherit: true,
      rules: [
        { token: "comment", foreground: "6A9955" },
        { token: "keyword", foreground: "C586C0" },
        { token: "type", foreground: "4EC9B0" },
        { token: "builtin", foreground: "DCDCAA" },
        { token: "string", foreground: "CE9178" },
        { token: "number", foreground: "B5CEA8" },
        { token: "operator", foreground: "D4D4D4" },
        { token: "color", foreground: "9CDCFE" },
        { token: "identifier", foreground: "9CDCFE" }
      ],
      colors: {
        "editor.background": "#111118",
        "editor.foreground": "#D4D4D4",
        "editor.lineHighlightBackground": "#1e1e2a",
        "editorCursor.foreground": "#8b5cf6",
        "editor.selectionBackground": "#264f78",
        "editorLineNumber.foreground": "#5A5A5A"
      }
    });

    monaco.editor.setTheme("pine-dark");
  };

  const copyToClipboard = () => {
    navigator.clipboard.writeText(value);
  };

  const downloadFile = () => {
    const blob = new Blob([value], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "strategy.pine";
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="flex flex-col h-full">
      {/* AI Generation Bar */}
      {onGenerate && (
        <div className="p-4 bg-background-tertiary border-b border-border-primary">
          <div className="flex gap-3">
            <input
              type="text"
              placeholder="Describe your strategy in plain English..."
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              className="flex-1 bg-background-secondary border border-border-primary rounded-lg px-4 py-2 text-text-primary placeholder:text-text-muted focus:outline-none focus:border-accent-primary"
            />
            <Button
              onClick={() => onGenerate(description)}
              disabled={isGenerating || !description.trim()}
              className="bg-accent-gradient"
            >
              <Wand2 className="h-4 w-4 mr-2" />
              {isGenerating ? "Generating..." : "Generate"}
            </Button>
          </div>
        </div>
      )}

      {/* Toolbar */}
      <div className="flex items-center justify-between px-4 py-2 bg-background-secondary border-b border-border-primary">
        <div className="flex items-center gap-2">
          <span className="text-sm text-text-muted font-mono">Pine Script v5</span>
          {validationErrors.length === 0 ? (
            <span className="flex items-center gap-1 text-success text-sm">
              <CheckCircle className="h-3 w-3" /> Valid
            </span>
          ) : (
            <span className="flex items-center gap-1 text-error text-sm">
              <AlertCircle className="h-3 w-3" /> {validationErrors.length} errors
            </span>
          )}
        </div>
        <div className="flex gap-2">
          <Button variant="ghost" size="sm" onClick={copyToClipboard}>
            <Copy className="h-4 w-4" />
          </Button>
          <Button variant="ghost" size="sm" onClick={downloadFile}>
            <Download className="h-4 w-4" />
          </Button>
        </div>
      </div>

      {/* Editor */}
      <div className="flex-1">
        <Editor
          height="100%"
          language="pinescript"
          value={value}
          onChange={(val) => onChange(val || "")}
          onMount={handleEditorDidMount}
          options={{
            fontSize: 14,
            fontFamily: "'JetBrains Mono', 'Fira Code', monospace",
            lineNumbers: "on",
            minimap: { enabled: false },
            scrollBeyondLastLine: false,
            automaticLayout: true,
            tabSize: 4,
            wordWrap: "on",
            padding: { top: 16, bottom: 16 }
          }}
        />
      </div>

      {/* Error Panel */}
      {validationErrors.length > 0 && (
        <div className="p-3 bg-error/10 border-t border-error/30">
          {validationErrors.map((error, i) => (
            <div key={i} className="flex items-center gap-2 text-sm text-error">
              <AlertCircle className="h-4 w-4" />
              {error}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
