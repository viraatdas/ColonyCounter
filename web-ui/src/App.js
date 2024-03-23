import React from 'react';
import './App.css';
import ImageUpload from './components/ImageUpload';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Colony Counter</h1>
        <main>
        <ImageUpload />
      </main>
      </header>
     
    </div>
  );
}

export default App;
