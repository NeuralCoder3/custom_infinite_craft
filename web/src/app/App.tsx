import React, { useCallback, useState } from 'react';
import logo from './logo.svg';
import './App.css';
import './api';
import { DndProvider } from 'react-dnd';
import { HTML5Backend } from 'react-dnd-html5-backend';
// import { Example } from './drag/Example';
// import { BasicSetup as Example } from './dnd/Example';
import { App as Example } from './dnd2/Example';

function App() {

  return (
    <div className="App">
				<DndProvider backend={HTML5Backend}>
					<Example />
				</DndProvider>
      {/* <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.tsx</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header> */}
    </div>
  );
}

export default App;
