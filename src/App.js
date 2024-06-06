import React, { useState } from 'react';
import './App.css';

function App() {
  const [instagramPageUrl, setInstagramPageUrl] = useState('');
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
          <div className="input-group">
            <input
              type="text"
              className="form-control"
              id="instagramPageUrl"
              value={instagramPageUrl}
              onChange={(e) => setInstagramPageUrl(e.target.value)}
              placeholder="Enter Instagram page URL"
              required
            />
            <button type="submit" className="btn btn-primary">Download Reels</button>
          </div>
        </div>
      </form>
      {message && <p className="mt-3">{message}</p>}
      <footer className="footer">
        <h2>Made by Karchev</h2>
      </footer>
    </div>
  );
}

export default App;
