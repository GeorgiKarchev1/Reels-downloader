import React, { useState } from 'react';
import './App.css';

function App() {
  const [instagramPageUrl, setInstagramPageUrl] = useState('');
  const [browserChoice, setBrowserChoice] = useState('chrome');
  const [message, setMessage] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    const response = await fetch('http://127.0.0.1:5000/download_reels', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        instagram_page_url: instagramPageUrl,
        browser_choice: browserChoice,
      }),
    });
    const data = await response.json();
    setMessage(data.message);
  };

  return (
    <div className="container">
      <h1 className="mt-5">Download Instagram Reels</h1>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="instagramPageUrl">Instagram Page URL</label>
          <input
            type="text"
            className="form-control"
            id="instagramPageUrl"
            value={instagramPageUrl}
            onChange={(e) => setInstagramPageUrl(e.target.value)}
            placeholder="Enter Instagram page URL"
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="browserChoice">Browser</label>
          <select
            className="form-control"
            id="browserChoice"
            value={browserChoice}
            onChange={(e) => setBrowserChoice(e.target.value)}
          >
            <option value="chrome">Chrome</option>
            <option value="firefox">Firefox</option>
            <option value="edge">Edge</option>
          </select>
        </div>
        <button type="submit" className="btn btn-primary">Download Reels</button>
      </form>
      {message && <p className="mt-3">{message}</p>}
    </div>
  );
}

export default App;

