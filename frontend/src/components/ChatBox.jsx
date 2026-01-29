import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import Message from './Message';
import Loader from './Loader';

const API_BASE_URL = 'http://localhost:8000';

const ChatBox = () => {
  const [messages, setMessages] = useState([
    {
      role: 'bot',
      text: 'Welcome to RagZen. Upload a PDF document and I shall assist you with any questions about its contents.',
    },
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const messagesEndRef = useRef(null);
  const fileInputRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage = { role: 'user', text: input };
    const questionText = input;
    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setLoading(true);
    setError(null);

    try {
      const response = await axios.post(`${API_BASE_URL}/ask`, {
        question: questionText,
      });

      const botMessage = {
        role: 'bot',
        text: response.data.answer,
        sources: response.data.sources,
      };

      setMessages((prev) => [...prev, botMessage]);
    } catch (err) {
      const errorMessage = err.response?.data?.detail || err.message || 'Error fetching response. Please check if the backend is running.';
      setError(errorMessage);
      setMessages((prev) => [
        ...prev,
        {
          role: 'bot',
          text: `Unable to process your request: ${errorMessage}`,
          isError: true,
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleFileUpload = async (e) => {
    const selectedFile = e.target.files[0];
    if (!selectedFile) return;

    if (!selectedFile.name.toLowerCase().endsWith('.pdf')) {
      alert('Please upload a PDF file');
      return;
    }

    setFile(selectedFile);
    setUploading(true);
    setError(null);

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const response = await axios.post(`${API_BASE_URL}/load_pdf`, formData);

      setMessages((prev) => [
        ...prev,
        {
          role: 'bot',
          text: `Document "${selectedFile.name}" has been uploaded successfully.\n\n${response.data.chunks_stored} text segments have been indexed and are ready for inquiry.`,
          isSuccess: true,
        },
      ]);
    } catch (err) {
      const errorMessage = err.response?.data?.detail || err.message || 'Error uploading file. Please check if the backend is running.';
      setError(errorMessage);
      setMessages((prev) => [
        ...prev,
        {
          role: 'bot',
          text: `Upload failed: ${errorMessage}`,
          isError: true,
        },
      ]);
    } finally {
      setUploading(false);
      setFile(null);
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="flex flex-col h-screen" style={{ backgroundColor: '#faf9f7' }}>
      {/* Header */}
      <header className="bg-white border-b" style={{ borderColor: '#e8e4dc' }}>
        <div className="max-w-4xl mx-auto px-6 py-5">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              {/* Classic Logo */}
              <div
                className="w-12 h-12 rounded-full flex items-center justify-center"
                style={{ backgroundColor: '#1e3a5f', boxShadow: '0 2px 8px rgba(30, 58, 95, 0.2)' }}
              >
                <span className="text-xl font-bold" style={{ color: '#d4af37', fontFamily: 'Georgia, serif' }}>R</span>
              </div>
              <div>
                <h1
                  className="text-2xl font-semibold tracking-wide"
                  style={{ color: '#1e3a5f', fontFamily: 'Georgia, serif' }}
                >
                  RagZen
                </h1>
                <p className="text-sm" style={{ color: '#8b7355', fontFamily: 'Georgia, serif' }}>
                  Document Intelligence
                </p>
              </div>
            </div>
            <div className="flex items-center">
              <input
                ref={fileInputRef}
                type="file"
                accept=".pdf"
                onChange={handleFileUpload}
                className="hidden"
                id="file-upload"
              />
              <label
                htmlFor="file-upload"
                className={`inline-flex items-center px-5 py-2.5 rounded text-sm font-medium cursor-pointer transition-all duration-300 ${
                  uploading ? 'cursor-not-allowed' : ''
                }`}
                style={{
                  backgroundColor: uploading ? '#e8e4dc' : '#1e3a5f',
                  color: uploading ? '#8b7355' : '#ffffff',
                  fontFamily: 'Georgia, serif',
                  boxShadow: uploading ? 'none' : '0 2px 6px rgba(30, 58, 95, 0.25)',
                }}
              >
                {uploading ? (
                  <>
                    <svg className="animate-spin -ml-1 mr-2 h-4 w-4" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Uploading...
                  </>
                ) : (
                  <>
                    <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 13h6m-3-3v6m5 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                    Upload PDF
                  </>
                )}
              </label>
            </div>
          </div>
        </div>
      </header>

      {/* Messages Area */}
      <main className="flex-1 overflow-y-auto">
        <div className="max-w-4xl mx-auto px-6 py-8">
          <div className="space-y-2">
            {messages.map((msg, i) => (
              <Message key={i} message={msg} index={i} />
            ))}
            {loading && <Loader />}
            <div ref={messagesEndRef} />
          </div>
        </div>
      </main>

      {/* Input Area */}
      <footer className="bg-white border-t" style={{ borderColor: '#e8e4dc' }}>
        <div className="max-w-4xl mx-auto px-6 py-5">
          <div className="flex items-end space-x-4">
            <div className="flex-1">
              <textarea
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Type your question here..."
                className="w-full rounded px-4 py-3 resize-none transition-all duration-300"
                style={{
                  backgroundColor: '#f5f4f2',
                  border: '1px solid #e8e4dc',
                  color: '#2c3e50',
                  fontFamily: 'Georgia, serif',
                  fontSize: '15px',
                }}
                onFocus={(e) => {
                  e.target.style.borderColor = '#1e3a5f';
                  e.target.style.backgroundColor = '#ffffff';
                }}
                onBlur={(e) => {
                  e.target.style.borderColor = '#e8e4dc';
                  e.target.style.backgroundColor = '#f5f4f2';
                }}
                rows="2"
                disabled={loading}
              />
            </div>
            <button
              onClick={handleSend}
              disabled={loading || !input.trim()}
              className="px-6 py-3 rounded font-medium transition-all duration-300"
              style={{
                backgroundColor: loading || !input.trim() ? '#e8e4dc' : '#1e3a5f',
                color: loading || !input.trim() ? '#8b7355' : '#ffffff',
                fontFamily: 'Georgia, serif',
                cursor: loading || !input.trim() ? 'not-allowed' : 'pointer',
                boxShadow: loading || !input.trim() ? 'none' : '0 2px 6px rgba(30, 58, 95, 0.25)',
              }}
            >
              Send
            </button>
          </div>
          <p
            className="text-xs mt-3 text-center"
            style={{ color: '#a89880', fontFamily: 'Georgia, serif' }}
          >
            Press Enter to send &middot; Shift+Enter for new line
          </p>
        </div>
      </footer>
    </div>
  );
};

export default ChatBox;
