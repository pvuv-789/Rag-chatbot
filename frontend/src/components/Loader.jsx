import React from 'react';

const Loader = () => {
  return (
    <div className="flex justify-start mb-5 animate-fade-in">
      <div className="flex items-start gap-4">
        {/* Avatar */}
        <div className="flex-shrink-0">
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
        </div>

        {/* Typing Indicator */}
        <div
          className="px-5 py-4 rounded-lg"
          style={{
            backgroundColor: '#ffffff',
            border: '1px solid #e8e4dc',
            boxShadow: '0 2px 8px rgba(0, 0, 0, 0.06)',
          }}
        >
          <div className="flex items-center gap-3">
            <div className="flex space-x-1.5">
              <div
                className="w-2 h-2 rounded-full animate-bounce"
                style={{ backgroundColor: '#1e3a5f', animationDelay: '0ms', animationDuration: '0.8s' }}
              ></div>
              <div
                className="w-2 h-2 rounded-full animate-bounce"
                style={{ backgroundColor: '#8b7355', animationDelay: '150ms', animationDuration: '0.8s' }}
              ></div>
              <div
                className="w-2 h-2 rounded-full animate-bounce"
                style={{ backgroundColor: '#d4af37', animationDelay: '300ms', animationDuration: '0.8s' }}
              ></div>
            </div>
            <span
              className="text-sm ml-1"
              style={{ color: '#8b7355', fontFamily: 'Georgia, serif' }}
            >
              Composing response...
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Loader;
