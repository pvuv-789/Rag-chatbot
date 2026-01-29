import React from 'react';

const Message = ({ message, index }) => {
  const isUser = message.role === 'user';

  return (
    <div
      className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-5 animate-fade-in`}
      style={{ animationDelay: `${index * 50}ms` }}
    >
      <div className={`max-w-2xl ${isUser ? 'order-1' : 'order-2'}`}>
        <div className={`flex items-start gap-4 ${isUser ? 'flex-row-reverse' : 'flex-row'}`}>
          {/* Avatar */}
          <div className="flex-shrink-0">
            {isUser ? (
              <div
                className="w-10 h-10 rounded-full flex items-center justify-center"
                style={{ backgroundColor: '#2c3e50' }}
              >
                <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
              </div>
            ) : (
              <div
                className="w-10 h-10 rounded-full flex items-center justify-center"
                style={{ backgroundColor: '#1e3a5f', boxShadow: '0 2px 6px rgba(30, 58, 95, 0.2)' }}
              >
                <span
                  className="text-base font-bold"
                  style={{ color: '#d4af37', fontFamily: 'Georgia, serif' }}
                >
                  R
                </span>
              </div>
            )}
          </div>

          {/* Message Content */}
          <div
            className="px-5 py-4 rounded-lg"
            style={{
              backgroundColor: isUser
                ? '#1e3a5f'
                : message.isError
                ? '#fef2f2'
                : message.isSuccess
                ? '#f0fdf4'
                : '#ffffff',
              color: isUser
                ? '#ffffff'
                : message.isError
                ? '#991b1b'
                : message.isSuccess
                ? '#166534'
                : '#2c3e50',
              border: isUser ? 'none' : '1px solid',
              borderColor: message.isError
                ? '#fecaca'
                : message.isSuccess
                ? '#bbf7d0'
                : '#e8e4dc',
              boxShadow: '0 2px 8px rgba(0, 0, 0, 0.06)',
              fontFamily: 'Georgia, serif',
            }}
          >
            <div className="whitespace-pre-wrap break-words text-sm leading-relaxed">
              {message.isError && (
                <span className="inline-flex items-center mr-2">
                  <svg className="w-4 h-4" style={{ color: '#991b1b' }} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                  </svg>
                </span>
              )}
              {message.isSuccess && (
                <span className="inline-flex items-center mr-2">
                  <svg className="w-4 h-4" style={{ color: '#166534' }} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </span>
              )}
              {message.text}
            </div>

            {/* Sources Section */}
            {message.sources && message.sources.length > 0 && (
              <div className="mt-4 pt-4" style={{ borderTop: '1px solid #e8e4dc' }}>
                <details className="group cursor-pointer">
                  <summary
                    className="text-xs font-medium transition-colors flex items-center gap-2"
                    style={{ color: '#8b7355' }}
                  >
                    <svg
                      className="w-3 h-3 transition-transform group-open:rotate-90"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                    </svg>
                    View {message.sources.length} source{message.sources.length > 1 ? 's' : ''}
                  </summary>
                  <div className="mt-3 space-y-3">
                    {message.sources.map((source, idx) => (
                      <div
                        key={idx}
                        className="text-xs p-3 rounded"
                        style={{
                          backgroundColor: '#f5f4f2',
                          border: '1px solid #e8e4dc',
                          fontFamily: 'Georgia, serif',
                        }}
                      >
                        <div className="flex items-center gap-2 mb-2">
                          <span
                            className="inline-flex items-center justify-center w-5 h-5 rounded-full text-xs font-medium"
                            style={{ backgroundColor: '#1e3a5f', color: '#d4af37' }}
                          >
                            {idx + 1}
                          </span>
                          <span className="font-medium" style={{ color: '#1e3a5f' }}>Reference</span>
                        </div>
                        <p style={{ color: '#5c5c5c' }} className="leading-relaxed">
                          {source.substring(0, 200)}...
                        </p>
                      </div>
                    ))}
                  </div>
                </details>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Message;
