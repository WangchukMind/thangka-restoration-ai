import React, { useState, useEffect } from 'react';
import { Upload, Settings, BookOpen, Gallery, History, HelpCircle, Play, Download, Share2, Star } from 'lucide-react';
import './KioskInterface.css';

const KioskInterface = () => {
  const [currentView, setCurrentView] = useState('home');
  const [uploadedImage, setUploadedImage] = useState(null);
  const [repairMode, setRepairMode] = useState('beginner');
  const [isRepairing, setIsRepairing] = useState(false);
  const [repairProgress, setRepairProgress] = useState(0);
  const [repairResult, setRepairResult] = useState(null);
  const [culturalInfo, setCulturalInfo] = useState(null);

  // 文化知识数据
  const culturalKnowledge = [
    {
      id: 'thangka_origin',
      title: '唐卡的起源',
      content: '唐卡是藏传佛教特有的绘画艺术，起源于7世纪，用于宗教仪式和教学。',
      image: '📿',
      color: '#FFD700'
    },
    {
      id: 'repair_meaning',
      title: '修复的意义',
      content: '唐卡修复不仅是技术活，更是对文化遗产的尊重和传承。',
      image: '🔧',
      color: '#DC143C'
    },
    {
      id: 'modern_tech',
      title: '现代技术',
      content: 'AI技术帮助我们更好地保护和传承这一珍贵的文化遗产。',
      image: '🤖',
      color: '#4169E1'
    }
  ];

  // 修复模式配置
  const repairModes = [
    {
      id: 'beginner',
      name: '新手模式',
      description: '全自动修复',
      icon: '🌟',
      color: '#4CAF50'
    },
    {
      id: 'standard',
      name: '标准模式',
      description: '智能修复',
      icon: '⚡',
      color: '#FF9800'
    },
    {
      id: 'professional',
      name: '专业模式',
      description: '精细修复',
      icon: '🎨',
      color: '#9C27B0'
    }
  ];

  // 主功能模块
  const mainModules = [
    {
      id: 'upload',
      title: '上传图片',
      icon: Upload,
      color: '#FFD700',
      description: '选择要修复的唐卡图片'
    },
    {
      id: 'repair',
      title: '修复模式',
      icon: Settings,
      color: '#DC143C',
      description: '选择修复模式'
    },
    {
      id: 'culture',
      title: '文化学习',
      icon: BookOpen,
      color: '#4169E1',
      description: '学习唐卡文化知识'
    },
    {
      id: 'gallery',
      title: '我的作品',
      icon: Gallery,
      color: '#8A2BE2',
      description: '查看修复作品'
    },
    {
      id: 'history',
      title: '修复历史',
      icon: History,
      color: '#FF5722',
      description: '查看修复记录'
    },
    {
      id: 'help',
      title: '帮助中心',
      icon: HelpCircle,
      color: '#607D8B',
      description: '使用帮助和支持'
    }
  ];

  // 处理图片上传
  const handleImageUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        setUploadedImage(e.target.result);
        setCurrentView('repair');
      };
      reader.readAsDataURL(file);
    }
  };

  // 开始修复
  const startRepair = async () => {
    setIsRepairing(true);
    setRepairProgress(0);
    
    // 模拟修复过程
    const interval = setInterval(() => {
      setRepairProgress(prev => {
        if (prev >= 100) {
          clearInterval(interval);
          setIsRepairing(false);
          setRepairResult(uploadedImage);
          setCulturalInfo(culturalKnowledge[0]);
          return 100;
        }
        return prev + 10;
      });
    }, 200);
  };

  // 渲染主界面
  const renderHomeView = () => (
    <div className="kiosk-home">
      <div className="welcome-section">
        <h1 className="welcome-title">🎨 唐卡修复大师</h1>
        <p className="welcome-subtitle">AI智能修复系统 - 让科技守护千年文化</p>
      </div>
      
      <div className="modules-grid">
        {mainModules.map(module => (
          <div
            key={module.id}
            className="module-card"
            style={{ '--module-color': module.color }}
            onClick={() => {
              if (module.id === 'upload') {
                document.getElementById('file-input').click();
              } else {
                setCurrentView(module.id);
              }
            }}
          >
            <div className="module-icon">
              <module.icon size={32} />
            </div>
            <h3 className="module-title">{module.title}</h3>
            <p className="module-description">{module.description}</p>
          </div>
        ))}
      </div>
      
      <input
        id="file-input"
        type="file"
        accept="image/*"
        onChange={handleImageUpload}
        style={{ display: 'none' }}
      />
    </div>
  );

  // 渲染修复界面
  const renderRepairView = () => (
    <div className="kiosk-repair">
      <div className="repair-header">
        <h2>AI智能修复</h2>
        <button 
          className="back-btn"
          onClick={() => setCurrentView('home')}
        >
          ← 返回
        </button>
      </div>
      
      {uploadedImage && (
        <div className="image-preview">
          <img src={uploadedImage} alt="上传的图片" />
        </div>
      )}
      
      <div className="repair-modes">
        <h3>选择修复模式</h3>
        <div className="modes-grid">
          {repairModes.map(mode => (
            <div
              key={mode.id}
              className={`mode-card ${repairMode === mode.id ? 'selected' : ''}`}
              style={{ '--mode-color': mode.color }}
              onClick={() => setRepairMode(mode.id)}
            >
              <div className="mode-icon">{mode.icon}</div>
              <h4>{mode.name}</h4>
              <p>{mode.description}</p>
            </div>
          ))}
        </div>
      </div>
      
      <div className="repair-actions">
        <button 
          className="repair-btn"
          onClick={startRepair}
          disabled={isRepairing}
        >
          {isRepairing ? (
            <>
              <div className="spinner"></div>
              修复中... {repairProgress}%
            </>
          ) : (
            <>
              <Play size={20} />
              开始修复
            </>
          )}
        </button>
      </div>
      
      {isRepairing && (
        <div className="progress-section">
          <div className="progress-bar">
            <div 
              className="progress-fill" 
              style={{ width: `${repairProgress}%` }}
            ></div>
          </div>
          <p className="progress-text">AI正在分析唐卡并修复损坏区域...</p>
        </div>
      )}
      
      {repairResult && (
        <div className="result-section">
          <h3>修复完成！</h3>
          <div className="result-comparison">
            <div className="result-item">
              <h4>修复前</h4>
              <img src={uploadedImage} alt="修复前" />
            </div>
            <div className="result-item">
              <h4>修复后</h4>
              <img src={repairResult} alt="修复后" />
            </div>
          </div>
          <div className="result-actions">
            <button className="action-btn download">
              <Download size={20} />
              下载
            </button>
            <button className="action-btn share">
              <Share2 size={20} />
              分享
            </button>
          </div>
        </div>
      )}
    </div>
  );

  // 渲染文化学习界面
  const renderCultureView = () => (
    <div className="kiosk-culture">
      <div className="culture-header">
        <h2>唐卡文化知识</h2>
        <button 
          className="back-btn"
          onClick={() => setCurrentView('home')}
        >
          ← 返回
        </button>
      </div>
      
      <div className="knowledge-cards">
        {culturalKnowledge.map(knowledge => (
          <div 
            key={knowledge.id}
            className="knowledge-card"
            style={{ '--card-color': knowledge.color }}
          >
            <div className="knowledge-icon">{knowledge.image}</div>
            <h3>{knowledge.title}</h3>
            <p>{knowledge.content}</p>
          </div>
        ))}
      </div>
    </div>
  );

  // 渲染实时信息区域
  const renderInfoArea = () => (
    <div className="info-area">
      {isRepairing && (
        <div className="progress-info">
          <h4>修复进度</h4>
          <div className="progress-bar">
            <div 
              className="progress-fill" 
              style={{ width: `${repairProgress}%` }}
            ></div>
          </div>
          <p>{repairProgress}% 完成</p>
        </div>
      )}
      
      {culturalInfo && (
        <div className="cultural-info">
          <h4>文化知识</h4>
          <div className="cultural-card">
            <div className="cultural-icon">{culturalInfo.image}</div>
            <h5>{culturalInfo.title}</h5>
            <p>{culturalInfo.content}</p>
          </div>
        </div>
      )}
    </div>
  );

  return (
    <div className="kiosk-container">
      {/* 头部 */}
      <header className="kiosk-header">
        <div className="header-logo">
          <span className="logo-icon">🎨</span>
          <span className="logo-text">唐卡修复大师</span>
        </div>
        <div className="header-info">
          <span className="time-info">17:42 23</span>
          <span className="weather-info">☀️ 22°C</span>
        </div>
      </header>

      {/* 主要内容区域 */}
      <main className="kiosk-main">
        <div className="main-content">
          {currentView === 'home' && renderHomeView()}
          {currentView === 'repair' && renderRepairView()}
          {currentView === 'culture' && renderCultureView()}
        </div>
        
        {/* 侧边信息区域 */}
        <aside className="sidebar">
          {renderInfoArea()}
        </aside>
      </main>

      {/* 底部状态栏 */}
      <footer className="kiosk-footer">
        <div className="footer-info">
          <span>AI智能修复系统 v1.0</span>
          <span>技术支持: Wangchuk Mind</span>
        </div>
        <div className="footer-actions">
          <button className="footer-btn">设置</button>
          <button className="footer-btn">帮助</button>
        </div>
      </footer>
    </div>
  );
};

export default KioskInterface;
