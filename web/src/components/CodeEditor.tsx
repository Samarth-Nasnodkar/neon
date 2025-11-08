import * as React from 'react';
import Editor from '@monaco-editor/react'


export function CodeEditor () {
  return (
    <div>
      <Editor
        height="90vh"
        defaultLanguage="python"
        defaultValue="// some comment"
      />
    </div>
  );
}

export default CodeEditor;
