import React, { useState } from 'react';
import { Upload, Play, Download, Heart, Share2, BookOpen, Users, Star } from 'lucide-react';
import './MVPHome.css';

const MVPHome = () => {
  const [uploadedImage, setUploadedImage] = useState(null);
  const [repairMode, setRepairMode] = useState('beginner');
  const [isRepairing, setIsRepairing] = useState(false);
  const [repairProgress, setRepairProgress] = useState(0);
  const [repairResult, setRepairResult] = useState(null);

  const repairModes = [
    {
      id: 'beginner',
      name: '新手模式',
      description: '全自动修复，适合初次使用',
      icon: '🌟',
      features: ['自动识别损坏区域', '一键修复', '快速处理']
    },
    {
      id: 'standard',
      name: '标准模式',
      description: '智能修复，平衡质量与速度',
      icon: '⚡',
      features: ['智能参数调整', '高质量修复', '文化知识介绍']
    },
    {
      id: 'professional',
      name: '专业模式',
      description: '精细修复，专业级效果',
      icon: '🎨',
      features: ['高级参数控制', '最高质量', '批量处理']
    }
  ];

  const handleImageUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        setUploadedImage(e.target.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const startRepair = async () => {
    if (!uploadedImage) return;
    
    setIsRepairing(true);
    setRepairProgress(0);
    
    // 模拟修复过程
    const interval = setInterval(() => {
      setRepairProgress(prev => {
        if (prev >= 100) {
          clearInterval(interval);
          setIsRepairing(false);
          setRepairResult(uploadedImage); // 模拟修复结果
          return 100;
        }
        return prev + 10;
      });
    }, 200);
  };

  const culturalFacts = [
    {
      title: "唐卡的起源",
      content: "唐卡是藏传佛教特有的绘画艺术，起源于7世纪，用于宗教仪式和教学。",
      image: "📿"
    },
    {
      title: "修复的意义",
      content: "唐卡修复不仅是技术活，更是对文化遗产的尊重和传承。",
      image: "🔧"
    },
    {
      title: "现代技术",
      content: "AI技术帮助我们更好地保护和传承这一珍贵的文化遗产。",
      image: "🤖"
    }
  ];

  return (
    <div className="mvp-home">
      {/* 头部导航 */}
      <header className="mvp-header">
        <div className="logo">
          <span className="logo-icon">🎨</span>
          <span className="logo-text">唐卡修复大师</span>
        </div>
        <nav className="nav-menu">
          <a href="#home">首页</a>
          <a href="#repair">修复</a>
          <a href="#culture">文化</a>
          <a href="#about">关于</a>
        </nav>
      </header>

      {/* 主要内容区域 */}
      <main className="mvp-main">
        {/* 英雄区域 */}
        <section className="hero-section">
          <div className="hero-content">
            <h1 className="hero-title">
              让AI守护千年唐卡艺术
            </h1>
            <p className="hero-subtitle">
              上传您的唐卡图片，AI智能识别并修复损坏区域，同时学习唐卡文化知识
            </p>
            
            {/* 快速开始区域 */}
            <div className="quick-start">
              <div className="upload-area">
                {!uploadedImage ? (
                  <div className="upload-placeholder">
                    <Upload size={48} />
                    <p>拖拽或点击上传唐卡图片</p>
                    <input
                      type="file"
                      accept="image/*"
                      onChange={handleImageUpload}
                      className="file-input"
                    />
                  </div>
                ) : (
                  <div className="image-preview">
                    <img src={uploadedImage} alt="上传的图片" />
                    <button 
                      className="change-image-btn"
                      onClick={() => setUploadedImage(null)}
                    >
                      更换图片
                    </button>
                  </div>
                )}
              </div>

              {/* 修复模式选择 */}
              {uploadedImage && (
                <div className="repair-modes">
                  <h3>选择修复模式</h3>
                  <div className="mode-cards">
                    {repairModes.map(mode => (
                      <div 
                        key={mode.id}
                        className={`mode-card ${repairMode === mode.id ? 'selected' : ''}`}
                        onClick={() => setRepairMode(mode.id)}
                      >
                        <div className="mode-icon">{mode.icon}</div>
                        <h4>{mode.name}</h4>
                        <p>{mode.description}</p>
                        <ul className="mode-features">
                          {mode.features.map((feature, index) => (
                            <li key={index}>{feature}</li>
                          ))}
                        </ul>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* 开始修复按钮 */}
              {uploadedImage && (
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
              )}

              {/* 修复进度 */}
              {isRepairing && (
                <div className="progress-section">
                  <div className="progress-bar">
                    <div 
                      className="progress-fill" 
                      style={{ width: `${repairProgress}%` }}
                    ></div>
                  </div>
                  <p className="progress-text">
                    AI正在分析唐卡并修复损坏区域...
                  </p>
                </div>
              )}

              {/* 修复结果 */}
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
                    <button className="download-btn">
                      <Download size={20} />
                      下载修复结果
                    </button>
                    <button className="share-btn">
                      <Share2 size={20} />
                      分享作品
                    </button>
                  </div>
                </div>
              )}
            </div>
          </div>
        </section>

        {/* 文化知识区域 */}
        <section className="culture-section">
          <h2>唐卡文化知识</h2>
          <div className="culture-cards">
            {culturalFacts.map((fact, index) => (
              <div key={index} className="culture-card">
                <div className="culture-icon">{fact.image}</div>
                <h3>{fact.title}</h3>
                <p>{fact.content}</p>
              </div>
            ))}
          </div>
        </section>

        {/* 产品特色 */}
        <section className="features-section">
          <h2>为什么选择我们</h2>
          <div className="features-grid">
            <div className="feature-item">
              <div className="feature-icon">⚡</div>
              <h3>一键修复</h3>
              <p>无需复杂设置，上传图片即可开始修复</p>
            </div>
            <div className="feature-item">
              <div className="feature-icon">🎨</div>
              <h3>文化学习</h3>
              <p>修复过程中学习唐卡文化知识</p>
            </div>
            <div className="feature-item">
              <div className="feature-icon">🤖</div>
              <h3>AI智能</h3>
              <p>先进AI技术确保修复质量</p>
            </div>
            <div className="feature-item">
              <div className="feature-icon">📱</div>
              <h3>简单易用</h3>
              <p>界面简洁，操作直观</p>
            </div>
          </div>
        </section>

        {/* 用户评价 */}
        <section className="testimonials-section">
          <h2>用户评价</h2>
          <div className="testimonials-grid">
            <div className="testimonial-card">
              <div className="stars">
                {[...Array(5)].map((_, i) => (
                  <Star key={i} size={16} fill="gold" />
                ))}
              </div>
              <p>"修复效果超出预期，还学到了很多唐卡知识！"</p>
              <div className="user-info">
                <div className="user-avatar">👤</div>
                <span>张女士</span>
              </div>
            </div>
            <div className="testimonial-card">
              <div className="stars">
                {[...Array(5)].map((_, i) => (
                  <Star key={i} size={16} fill="gold" />
                ))}
              </div>
              <p>"操作简单，修复质量很高，推荐给所有唐卡爱好者！"</p>
              <div className="user-info">
                <div className="user-avatar">👤</div>
                <span>李先生</span>
              </div>
            </div>
          </div>
        </section>
      </main>

      {/* 页脚 */}
      <footer className="mvp-footer">
        <div className="footer-content">
          <div className="footer-section">
            <h4>产品</h4>
            <ul>
              <li><a href="#features">功能特色</a></li>
              <li><a href="#pricing">价格方案</a></li>
              <li><a href="#api">API接口</a></li>
            </ul>
          </div>
          <div className="footer-section">
            <h4>文化</h4>
            <ul>
              <li><a href="#knowledge">唐卡知识</a></li>
              <li><a href="#history">历史传承</a></li>
              <li><a href="#artists">艺术家</a></li>
            </ul>
          </div>
          <div className="footer-section">
            <h4>支持</h4>
            <ul>
              <li><a href="#help">帮助中心</a></li>
              <li><a href="#contact">联系我们</a></li>
              <li><a href="#community">用户社区</a></li>
            </ul>
          </div>
        </div>
        <div className="footer-bottom">
          <p>&copy; 2024 唐卡修复大师. 让AI守护千年唐卡艺术</p>
        </div>
      </footer>
    </div>
  );
};

export default MVPHome;
