import React, { useState } from 'react';
import './App.css';
import KioskInterface from './components/KioskInterface';
import MVPHome from './pages/MVPHome';

function App() {
  const [viewMode, setViewMode] = useState('kiosk'); // 'kiosk' or 'web'

  return (
    <div className="App">
      {/* 模式切换按钮 */}
      <div className="mode-switcher">
        <button 
          className={`mode-btn ${viewMode === 'kiosk' ? 'active' : ''}`}
          onClick={() => setViewMode('kiosk')}
        >
          🖥️ 终端模式
        </button>
        <button 
          className={`mode-btn ${viewMode === 'web' ? 'active' : ''}`}
          onClick={() => setViewMode('web')}
        >
          🌐 网页模式
        </button>
      </div>

      {/* 根据模式渲染不同界面 */}
      {viewMode === 'kiosk' ? <KioskInterface /> : <MVPHome />}
    </div>
  );
}

export default App;
