import React, { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { TransitionWorkspace } from './App';

import './styles.css';


console.debug(TransitionWorkspace);

function initFrontend() {
  const appRoot = document.getElementById('app');
  if (appRoot) {
    if (!window.isSecureContext) {
      appRoot.innerText = "No secure context available";
      console.error("Can’t initialize the app: missing secure context");
      throw new Error("No secure context");
    } else {
      createRoot(appRoot).render(
        <StrictMode>
          <TransitionWorkspace />
        </StrictMode>
      );
    }
  } else {
    console.error("No root");
  }
}

initFrontend();
