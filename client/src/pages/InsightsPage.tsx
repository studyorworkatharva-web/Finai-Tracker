import React, { useState } from 'react';
import { AnimatedPage } from '../App';
import { Card } from '../components/ui/Card';
import { Input } from '../components/ui/Input';
import { Button } from '../components/ui/Button';
import { PaperAirplaneIcon, SparklesIcon } from '@heroicons/react/24/solid';
import { motion } from 'framer-motion';

// 

type Message = {
  sender: 'user' | 'ai';
  text: string;
};

export default function InsightsPage() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage: Message = { sender: 'user', text: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    // TODO: 
    // 1. Fetch recent transactions from transactionsApi
    // const txResponse = await transactionsApi.get('/?limit=20');
    // const context = txResponse.data.items;
    
    // 2. Send to AI API
    // const aiResponse = await aiApi.post('/insights/query', {
    //   user_prompt: input,
    //   transactions_context: context,
    // });
    // const aiMessage: Message = { sender: 'ai', text: aiResponse.data.insight };

    // Mock response
    await new Promise(res => setTimeout(res, 1500));
    const aiMessage: Message = { 
      sender: 'ai', 
      text: `Based on your recent spending, cutting your "Dining Out" category by 20% could save you an extra **$80/month**. This would put you on track to meet your "Vacation Fund" goal 2 months earlier.`
    };
    
    setMessages((prev) => [...prev, aiMessage]);
    setIsLoading(false);
  };

  return (
    <AnimatedPage>
      <div className="flex h-[calc(100vh-120px)] flex-col">
        {/* Header */}
        <div className="mb-6">
          <h1 className="font-serif text-4xl font-bold">AI Insights</h1>
          <p className="text-lg text-muted">
            Ask questions about your spending, goals, and more.
          </p>
        </div>
        
        {/* Chat Area */}
        <Card className="flex-1 flex flex-col p-0 overflow-hidden">
          <div className="flex-1 space-y-4 overflow-y-auto p-6">
            {/* Initial Message */}
            {messages.length === 0 && (
              <div className="text-center p-8">
                <SparklesIcon className="h-12 w-12 mx-auto text-primary" />
                <h3 className="mt-2 text-lg font-medium text-foreground">
                  Ask me anything
                </h3>
                <p className="mt-1 text-sm text-muted">
                  e.g., "Where am I spending the most money?" or "Suggest a budget for me."
                </p>
              </div>
            )}
            
            {/* Messages */}
            {messages.map((msg, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-xs md:max-w-md lg:max-w-lg rounded-lg px-4 py-3 ${
                    msg.sender === 'user'
                      ? 'bg-primary text-primary-foreground'
                      : 'glass-card border border-slate-200/50 dark:border-slate-800/50'
                  }`}
                >
                  <div className="prose prose-sm dark:prose-invert"
                       dangerouslySetInnerHTML={{ __html: msg.text }} />
                </div>
              </motion.div>
            ))}
            
            {/* Typing Indicator */}
            {isLoading && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="flex justify-start"
              >
                <div className="glass-card rounded-lg px-4 py-3 inline-flex items-center space-x-1">
                  <span className="h-2 w-2 animate-bounce rounded-full bg-muted [animation-delay:-0.3s]" />
                  <span className="h-2 w-2 animate-bounce rounded-full bg-muted [animation-delay:-0.15s]" />
                  <span className="h-2 w-2 animate-bounce rounded-full bg-muted" />
                </div>
              </motion.div>
            )}
          </div>
          
          {/* Input Form */}
          <div className="border-t border-slate-200/50 dark:border-slate-800/50 p-4 bg-background/50">
            <form onSubmit={handleSubmit} className="flex items-center space-x-2">
              <Input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Ask FinAI..."
                className="flex-1"
                disabled={isLoading}
              />
              <Button type="submit" variant="icon" aria-label="Send message" disabled={isLoading}>
                <PaperAirplaneIcon className="h-5 w-5" />
              </Button>
            </form>
          </div>
        </Card>
      </div>
    </AnimatedPage>
  );
}