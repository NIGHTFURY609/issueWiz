'use client';
import React, { useState } from 'react';
import ChatBot from './../components/chatbot';
import fetchDetails from '../utils/user_det';
import type { FetchedData } from '../utils/user_det';
import { GitBranch, Code2, Search, Github, FileText, Workflow } from 'lucide-react';

// Define the structure for chat messages in our application
interface ChatMessage {
  type: 'bot' | 'user';
  content: any;
}

// Define the structure for issue recommendations from the AI
interface Recommendation {
  issue_title: string;
  issue_url: string;
  difficulty_level: string;
  learning_opportunities: string;
  why_recommended: string;
}

const Beginner = () => {
  // State management for form inputs and application data
  const [username, setUsername] = useState<string>('');
  const [repoUrl, setRepoUrl] = useState<string>('');
  const [chatMessages, setChatMessages] = useState<ChatMessage[]>([]);
  const [showChatBot, setShowChatBot] = useState<boolean>(false);
  const [userMessage, setUserMessage] = useState<string>('');
  const [userData, setUserData] = useState<FetchedData | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);

  // Helper function to generate the appropriate initial message based on recommendations
  const generateInitialMessage = (recommendations: Recommendation[]) => {
    if (!recommendations || recommendations.length === 0) {
      return {
        type: 'bot' as const,
        content: `Hi there! 👋 I've analyzed your GitHub profile and the repository you provided, but I couldn't find any issues that perfectly match your current skills and interests. This could be because:

1. The available issues might require different technical skills than what's shown in your profile
2. The repository might not have any open issues at the moment
3. The existing issues might be too complex for a beginner

Don't worry though! Here are some suggestions for your next steps:

• Try exploring other beginner-friendly repositories
• Look for issues labeled with "good-first-issue" or "beginner-friendly"
• Consider contributing to documentation or testing
• Feel free to ask me about how to find more suitable repositories or how to prepare for your first contribution!

Would you like help finding other beginner-friendly repositories that match your skills? 😊`
      };
    }

    // Format recommendations with proper spacing and emojis
    const formattedRecommendations = recommendations.map(
      (rec: Recommendation) => `
        📌 ${rec.issue_title}
        🔗 ${rec.issue_url}
        📊 Difficulty: ${rec.difficulty_level}
        📚 Learning: ${rec.learning_opportunities}
        💡 Why: ${rec.why_recommended}
      `
    ).join('\n\n');

    // Return a personalized message based on the number of recommendations
    return {
      type: 'bot' as const,
      content: `Hi there! 👋 I'm excited to help you start your open source journey! I've analyzed your profile and found ${recommendations.length === 1 ? 'a perfect issue' : 'some perfect issues'} for beginners like you. Here ${recommendations.length === 1 ? 'is your' : 'are your'} hand-picked recommendation${recommendations.length === 1 ? '' : 's'}:\n\n${formattedRecommendations}\n\nDon't worry if this feels overwhelming - I'm here to guide you every step of the way! What would you like to know more about? You can ask me anything about ${recommendations.length === 1 ? 'this issue' : 'these issues'}, how to get started, or what skills you'll need. 😊`
    };
  };

  // Handle fetching user data and getting AI recommendations
  const handleFetch = async () => {
    if (!username || !repoUrl) return;
    
    setIsLoading(true);
    try {
      const data = await fetchDetails(username, repoUrl);
      
      if (data) {
        setUserData(data);
        const aiResponse = await fetch('/api/ai_suggest', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(data)
        });

        if (!aiResponse.ok) {
          const errorText = await aiResponse.text();
          console.error(`AI recommendation failed: ${errorText}`);
          return;
        }

        const aiRecommendations = await aiResponse.json();
        
        // Generate the appropriate initial message based on recommendations
        const initialMessage = generateInitialMessage(aiRecommendations.reply.recommendations);

        setChatMessages([initialMessage]);
        setShowChatBot(true);
      }
    } catch (err) {
      console.error('Full Fetch Error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  // Handle sending user messages in the chat interface
  const handleSendMessage = async () => {
    if (!userMessage.trim()) return;

    const newUserMessage: ChatMessage = {
      type: 'user',
      content: userMessage,
    };
    
    setChatMessages(prev => [...prev, newUserMessage]);
    setUserMessage('');

    // Prepare context for AI response
    const context = {
      userProfile: userData?.profile,
      previousMessages: chatMessages,
      currentQuery: userMessage,
      userRepos: userData?.repositories || [],
      technicalContext: {
        languages: [...new Set(userData?.repositories.map(repo => repo.language).filter(Boolean))],
        topics: [...new Set(userData?.repositories.flatMap(repo => repo.topics || []))],
      }
    };

    try {
      const aiResponse = await fetch('/api/chat_followup', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(context)
      });

      if (!aiResponse.ok) throw new Error('Failed to get AI response');
      
      const response = await aiResponse.json();
      
      const newBotMessage: ChatMessage = {
        type: 'bot',
        content: response.reply,
      };

      setChatMessages(prev => [...prev, newBotMessage]);
    } catch (error) {
      console.error('Chat follow-up error:', error);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#0B1A2E] via-[#12254A] to-[#0D1E3A] p-8 relative overflow-hidden">
      {/* Decorative background grid */}
      <div className="absolute inset-0 pointer-events-none opacity-10">
        <div className="absolute inset-0 bg-[linear-gradient(to_right,#0B1A2E_1px,transparent_1px),linear-gradient(to_bottom,#0B1A2E_1px,transparent_1px)] bg-[size:40px_40px]"></div>
      </div>

      {/* Decorative floating icons */}
      <div className="absolute top-20 right-20 opacity-20 max-md:hidden">
        <GitBranch size={100} className="text-cyan-500" />
      </div>
      <div className="absolute bottom-20 left-20 opacity-20 max-md:hidden">
        <Code2 size={100} className="text-cyan-500" />
      </div>
      <div className="absolute top-1/3 left-20 opacity-20 max-md:hidden">
        <FileText size={80} className="text-cyan-500" />
      </div>
      <div className="absolute bottom-1/3 right-20 opacity-20 max-md:hidden">
        <Workflow size={80} className="text-cyan-500" />
      </div>

      <div className="max-w-4xl mx-auto relative z-10">
        {!showChatBot ? (
          // Initial input form
          <div className="max-w-2xl mx-auto bg-[#162544]/50 backdrop-blur-xl rounded-2xl shadow-2xl p-8 border border-cyan-500/20">
            <div className="text-center space-y-6 mb-8">
              <div className="flex items-center justify-center space-x-4">
                <Search className="text-cyan-400" size={40} />
                <h1 className="text-4xl font-bold text-white">Repository and Issue Matcher</h1>
              </div>
              <p className="text-xl text-white/70">
                Enter your details below to discover tailored open-source issues that match your skills and interests.
              </p>
            </div>

            <div className="space-y-6">
              <div className="space-y-2">
                <label className="text-white/70 text-sm font-medium">GitHub Username</label>
                <div className="relative">
                  <Github className="absolute left-3 top-1/2 transform -translate-y-1/2 text-cyan-500/50" size={20} />
                  <input
                    type="text"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    placeholder="Enter your GitHub username"
                    className="w-full pl-10 p-4 rounded-xl bg-[#1E2B43]/50 border border-cyan-500/20 text-white 
                      focus:ring-2 focus:ring-cyan-500/40 focus:border-transparent"
                  />
                </div>
              </div>
              
              <div className="space-y-2">
                <label className="text-white/70 text-sm font-medium">Repository URL</label>
                <input
                  type="text"
                  value={repoUrl}
                  onChange={(e) => setRepoUrl(e.target.value)}
                  placeholder="Enter the repository link"
                  className="w-full p-4 rounded-xl bg-[#1E2B43]/50 border border-cyan-500/20 text-white 
                    focus:ring-2 focus:ring-cyan-500/40 focus:border-transparent"
                />
              </div>
              
              <button
                onClick={handleFetch}
                disabled={isLoading || !username || !repoUrl}
                className="w-full bg-gradient-to-r from-cyan-400 to-blue-500 text-white py-4 rounded-xl
                  hover:scale-105 transition-all duration-300 shadow-xl hover:shadow-cyan-500/50
                  disabled:opacity-50 disabled:hover:scale-100"
              >
                {isLoading ? 'Finding Issues...' : 'Find Recommended Issues'}
              </button>
            </div>
          </div>
        ) : (
          // Chat interface
          <ChatBot
            messages={chatMessages}
            userMessage={userMessage}
            onMessageChange={setUserMessage}
            onSendMessage={handleSendMessage}
          />
        )}
      </div>
    </div>
  );
};

export default Beginner;