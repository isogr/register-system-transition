import React from 'react';

declare module 'react' {
  namespace JSX {
    interface IntrinsicElements extends React.JSX.IntrinsicElements {
      'json-diff-viewer': any;
    }
  }
}
