/**
 * Landing Page Component
 */
import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Brain, TrendingUp, Target, Zap, ArrowRight } from 'lucide-react';

export default function Landing() {
  const navigate = useNavigate();
  
  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-500 via-primary-600 to-accent-600">
      {/* Hero Section */}
      <div className="relative overflow-hidden">
        {/* Animated background circles */}
        <div className="absolute top-20 left-10 w-72 h-72 bg-white/10 rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute bottom-20 right-10 w-96 h-96 bg-accent-400/20 rounded-full blur-3xl animate-pulse delay-1000"></div>
        
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-20 pb-32">
          {/* Logo */}
          <div className="flex items-center justify-center mb-8">
            <div className="w-16 h-16 bg-white/20 backdrop-blur-lg rounded-2xl flex items-center justify-center">
              <Brain size={32} className="text-white" />
            </div>
          </div>
          
          {/* Main Heading */}
          <div className="text-center mb-12">
            <h1 className="text-5xl sm:text-6xl lg:text-7xl font-bold text-white mb-6 leading-tight">
              Your Personal
              <span className="block bg-gradient-to-r from-yellow-200 to-orange-200 bg-clip-text text-transparent">
                AI Productivity Coach
              </span>
            </h1>
            <p className="text-xl sm:text-2xl text-white/90 max-w-3xl mx-auto leading-relaxed">
              ML-powered insights to optimize your habits, predict your productivity, 
              and help you achieve your goals
            </p>
          </div>
          
          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-20">
            <button
              onClick={() => navigate('/dashboard')}
              className="group bg-white text-primary-600 px-8 py-4 rounded-xl font-bold text-lg 
                       hover:bg-opacity-90 transition-all duration-200 
                       shadow-2xl hover:shadow-3xl hover:scale-105 active:scale-95
                       flex items-center space-x-2"
            >
              <span>Get Started</span>
              <ArrowRight size={20} className="group-hover:translate-x-1 transition-transform" />
            </button>
            <button
              onClick={() => navigate('/activity')}
              className="bg-white/10 backdrop-blur-lg text-white px-8 py-4 rounded-xl font-bold text-lg 
                       border-2 border-white/30 hover:bg-white/20 
                       transition-all duration-200 hover:scale-105 active:scale-95"
            >
              Log Activity
            </button>
          </div>
          
          {/* Feature Cards */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-5xl mx-auto">
            <FeatureCard
              icon={<Brain size={32} />}
              title="AI Predictions"
              description="24-hour productivity forecasting using machine learning"
            />
            <FeatureCard
              icon={<Target size={32} />}
              title="Pattern Recognition"
              description="Automatically discover your peak performance hours"
            />
            <FeatureCard
              icon={<Zap size={32} />}
              title="Smart Recommendations"
              description="Personalized suggestions tailored to your unique patterns"
            />
          </div>
        </div>
      </div>
      
      {/* Stats Section */}
      <div className="bg-white/10 backdrop-blur-lg border-t border-white/20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 text-center">
            <StatItem number="85%" label="Prediction Accuracy" />
            <StatItem number="45%" label="Productivity Increase" />
            <StatItem number="7+" label="Day Average Streak" />
          </div>
        </div>
      </div>
    </div>
  );
}

// Feature Card Component
function FeatureCard({ icon, title, description }) {
  return (
    <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-6 border border-white/20
                    hover:bg-white/15 transition-all duration-200 hover:scale-105">
      <div className="w-12 h-12 bg-white/20 rounded-xl flex items-center justify-center mb-4 text-white">
        {icon}
      </div>
      <h3 className="text-xl font-bold text-white mb-2">{title}</h3>
      <p className="text-white/80 leading-relaxed">{description}</p>
    </div>
  );
}

// Stat Item Component
function StatItem({ number, label }) {
  return (
    <div>
      <div className="text-4xl font-bold text-white mb-2">{number}</div>
      <div className="text-white/80">{label}</div>
    </div>
  );
}