import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import AuthPage from './pages/AuthPage';
import Dashboard from './pages/Dashboard';
import ChatPage from './pages/ChatPage';  
  
function App() {  
  // 简单的鉴权检查 (实际项目中应检查 Token 有效性)  
  const isAuthenticated = !!localStorage.getItem('token');  
  
  return (  
    <Router>  
      <Routes>  
        {/* 登录注册页 */}  
        <Route path="/auth" element={<AuthPage />} />  
          
        {/* 主功能面板 */}  
        <Route   
          path="/dashboard"   
          element={isAuthenticated ? <Dashboard /> : <Navigate to="/auth" />}   
        />  
  
        {/* 具体的聊天功能页，:featureId 是动态参数 */}  
        <Route   
          path="/feature/:featureId"   
          element={isAuthenticated ? <ChatPage /> : <Navigate to="/auth" />}   
        />  
  
        {/* 默认重定向 */}  
        <Route path="*" element={<Navigate to="/auth" />} />  
      </Routes>  
    </Router>  
  );  
}  
  
export default App;  
