import React from "react";
import "./App.css";
import ImageUpload from "./components/ImageUpload";

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <p className="description">
          Welcome to the Colony Counter application. Upload images of petri
          dishes to automatically count colonies.
        </p>
        <h1>Colony Counter</h1>
        <main>
          <ImageUpload />
        </main>
        <p className="description">
          <a
            href="https://github.com/viraatdas/ColonyCounter"
            target="_blank"
            rel="noopener noreferrer"
          >
            https://github.com/viraatdas/ColonyCounter
          </a>
        </p>
      </header>
    </div>
  );
}

export default App;
