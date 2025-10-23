#!/usr/bin/env python3
"""
唐卡修复大师MVP产品运营分析工具
用于监控产品使用情况和用户行为
Developed by Wangchuk Mind
"""

import json
import time
import sqlite3
from datetime import datetime, timedelta
from collections import defaultdict
import matplotlib.pyplot as plt
import pandas as pd

class MVPProductAnalytics:
    """MVP产品运营分析类"""
    
    def __init__(self, db_path="mvp_analytics.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """初始化数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 创建用户行为表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_actions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            action_type TEXT,
            action_data TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # 创建修复记录表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS repair_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            task_id TEXT,
            mode TEXT,
            success BOOLEAN,
            duration REAL,
            rating INTEGER,
            feedback TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # 创建文化知识访问表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS knowledge_views (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            knowledge_id TEXT,
            view_duration REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        conn.commit()
        conn.close()
    
    def track_user_action(self, user_id, action_type, action_data=None):
        """跟踪用户行为"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        INSERT INTO user_actions (user_id, action_type, action_data)
        VALUES (?, ?, ?)
        ''', (user_id, action_type, json.dumps(action_data) if action_data else None))
        
        conn.commit()
        conn.close()
    
    def track_repair(self, user_id, task_id, mode, success, duration, rating=None, feedback=None):
        """跟踪修复记录"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        INSERT INTO repair_records (user_id, task_id, mode, success, duration, rating, feedback)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, task_id, mode, success, duration, rating, feedback))
        
        conn.commit()
        conn.close()
    
    def track_knowledge_view(self, user_id, knowledge_id, view_duration):
        """跟踪文化知识访问"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        INSERT INTO knowledge_views (user_id, knowledge_id, view_duration)
        VALUES (?, ?, ?)
        ''', (user_id, knowledge_id, view_duration))
        
        conn.commit()
        conn.close()
    
    def get_daily_stats(self, days=7):
        """获取每日统计"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 每日用户数
        cursor.execute('''
        SELECT DATE(timestamp) as date, COUNT(DISTINCT user_id) as daily_users
        FROM user_actions
        WHERE timestamp >= datetime('now', '-{} days')
        GROUP BY DATE(timestamp)
        ORDER BY date
        '''.format(days))
        daily_users = cursor.fetchall()
        
        # 每日修复数
        cursor.execute('''
        SELECT DATE(timestamp) as date, COUNT(*) as daily_repairs
        FROM repair_records
        WHERE timestamp >= datetime('now', '-{} days')
        GROUP BY DATE(timestamp)
        ORDER BY date
        '''.format(days))
        daily_repairs = cursor.fetchall()
        
        # 每日文化知识访问
        cursor.execute('''
        SELECT DATE(timestamp) as date, COUNT(*) as daily_knowledge_views
        FROM knowledge_views
        WHERE timestamp >= datetime('now', '-{} days')
        GROUP BY DATE(timestamp)
        ORDER BY date
        '''.format(days))
        daily_knowledge = cursor.fetchall()
        
        conn.close()
        
        return {
            'daily_users': daily_users,
            'daily_repairs': daily_repairs,
            'daily_knowledge_views': daily_knowledge
        }
    
    def get_user_behavior_analysis(self):
        """用户行为分析"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 用户行为分布
        cursor.execute('''
        SELECT action_type, COUNT(*) as count
        FROM user_actions
        GROUP BY action_type
        ORDER BY count DESC
        ''')
        action_distribution = cursor.fetchall()
        
        # 修复模式偏好
        cursor.execute('''
        SELECT mode, COUNT(*) as count
        FROM repair_records
        GROUP BY mode
        ORDER BY count DESC
        ''')
        mode_preference = cursor.fetchall()
        
        # 用户留存率（7日）
        cursor.execute('''
        SELECT 
            COUNT(DISTINCT CASE WHEN first_action.date = last_action.date THEN first_action.user_id END) as retained_users,
            COUNT(DISTINCT first_action.user_id) as total_users
        FROM (
            SELECT user_id, MIN(DATE(timestamp)) as date
            FROM user_actions
            GROUP BY user_id
        ) first_action
        LEFT JOIN (
            SELECT user_id, MAX(DATE(timestamp)) as date
            FROM user_actions
            WHERE timestamp >= datetime('now', '-7 days')
            GROUP BY user_id
        ) last_action ON first_action.user_id = last_action.user_id
        ''')
        retention_data = cursor.fetchone()
        
        conn.close()
        
        return {
            'action_distribution': action_distribution,
            'mode_preference': mode_preference,
            'retention_rate': retention_data[0] / retention_data[1] if retention_data[1] > 0 else 0
        }
    
    def get_product_metrics(self):
        """产品关键指标"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 总用户数
        cursor.execute('SELECT COUNT(DISTINCT user_id) FROM user_actions')
        total_users = cursor.fetchone()[0]
        
        # 总修复数
        cursor.execute('SELECT COUNT(*) FROM repair_records')
        total_repairs = cursor.fetchone()[0]
        
        # 修复成功率
        cursor.execute('SELECT AVG(CASE WHEN success THEN 1 ELSE 0 END) FROM repair_records')
        success_rate = cursor.fetchone()[0] or 0
        
        # 平均评分
        cursor.execute('SELECT AVG(rating) FROM repair_records WHERE rating IS NOT NULL')
        avg_rating = cursor.fetchone()[0] or 0
        
        # 平均修复时间
        cursor.execute('SELECT AVG(duration) FROM repair_records WHERE success = 1')
        avg_duration = cursor.fetchone()[0] or 0
        
        # 文化知识访问数
        cursor.execute('SELECT COUNT(*) FROM knowledge_views')
        knowledge_views = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'total_users': total_users,
            'total_repairs': total_repairs,
            'success_rate': success_rate,
            'avg_rating': avg_rating,
            'avg_duration': avg_duration,
            'knowledge_views': knowledge_views
        }
    
    def generate_report(self):
        """生成运营报告"""
        print("📊 唐卡修复大师MVP产品运营报告")
        print("=" * 50)
        
        # 产品指标
        metrics = self.get_product_metrics()
        print(f"\n📈 产品指标:")
        print(f"  总用户数: {metrics['total_users']}")
        print(f"  总修复数: {metrics['total_repairs']}")
        print(f"  修复成功率: {metrics['success_rate']:.2%}")
        print(f"  平均评分: {metrics['avg_rating']:.1f}/5")
        print(f"  平均修复时间: {metrics['avg_duration']:.1f}秒")
        print(f"  文化知识访问: {metrics['knowledge_views']}次")
        
        # 用户行为分析
        behavior = self.get_user_behavior_analysis()
        print(f"\n👥 用户行为分析:")
        print(f"  7日留存率: {behavior['retention_rate']:.2%}")
        print(f"  修复模式偏好:")
        for mode, count in behavior['mode_preference']:
            print(f"    {mode}: {count}次")
        
        # 每日趋势
        daily_stats = self.get_daily_stats()
        print(f"\n📅 最近7天趋势:")
        print("  日期        用户数    修复数    文化访问")
        print("  " + "-" * 40)
        
        # 合并数据
        daily_data = {}
        for date, users in daily_stats['daily_users']:
            daily_data[date] = {'users': users, 'repairs': 0, 'knowledge': 0}
        
        for date, repairs in daily_stats['daily_repairs']:
            if date in daily_data:
                daily_data[date]['repairs'] = repairs
        
        for date, knowledge in daily_stats['daily_knowledge_views']:
            if date in daily_data:
                daily_data[date]['knowledge'] = knowledge
        
        for date in sorted(daily_data.keys()):
            data = daily_data[date]
            print(f"  {date}    {data['users']:4d}     {data['repairs']:4d}     {data['knowledge']:4d}")
    
    def create_visualizations(self):
        """创建可视化图表"""
        try:
            import matplotlib.pyplot as plt
            import pandas as pd
            
            # 获取数据
            daily_stats = self.get_daily_stats()
            behavior = self.get_user_behavior_analysis()
            
            # 创建图表
            fig, axes = plt.subplots(2, 2, figsize=(15, 10))
            fig.suptitle('唐卡修复大师MVP产品运营数据', fontsize=16)
            
            # 每日用户趋势
            dates = [item[0] for item in daily_stats['daily_users']]
            users = [item[1] for item in daily_stats['daily_users']]
            axes[0, 0].plot(dates, users, marker='o')
            axes[0, 0].set_title('每日活跃用户')
            axes[0, 0].set_ylabel('用户数')
            axes[0, 0].tick_params(axis='x', rotation=45)
            
            # 修复模式分布
            modes = [item[0] for item in behavior['mode_preference']]
            counts = [item[1] for item in behavior['mode_preference']]
            axes[0, 1].pie(counts, labels=modes, autopct='%1.1f%%')
            axes[0, 1].set_title('修复模式分布')
            
            # 每日修复数
            repairs = [item[1] for item in daily_stats['daily_repairs']]
            axes[1, 0].bar(dates, repairs)
            axes[1, 0].set_title('每日修复数')
            axes[1, 0].set_ylabel('修复数')
            axes[1, 0].tick_params(axis='x', rotation=45)
            
            # 文化知识访问
            knowledge = [item[1] for item in daily_stats['daily_knowledge_views']]
            axes[1, 1].plot(dates, knowledge, marker='s', color='green')
            axes[1, 1].set_title('每日文化知识访问')
            axes[1, 1].set_ylabel('访问数')
            axes[1, 1].tick_params(axis='x', rotation=45)
            
            plt.tight_layout()
            plt.savefig('mvp_analytics_report.png', dpi=300, bbox_inches='tight')
            print("📊 可视化图表已保存: mvp_analytics_report.png")
            
        except ImportError:
            print("⚠️ 需要安装matplotlib和pandas来生成可视化图表")
            print("运行: pip install matplotlib pandas")

def main():
    """主函数"""
    analytics = MVPProductAnalytics()
    
    # 生成报告
    analytics.generate_report()
    
    # 创建可视化
    analytics.create_visualizations()
    
    print("\n✅ 运营分析完成！")

if __name__ == "__main__":
    main()
