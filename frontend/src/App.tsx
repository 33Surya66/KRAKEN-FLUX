import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider, CssBaseline } from '@mui/material';
import theme from './theme';
import Layout from './components/Layout/Layout';
import Dashboard from './pages/Dashboard/Dashboard';
import ThreatDetection from './pages/ThreatDetection/ThreatDetection';
import Analytics from './pages/Analytics/Analytics';

const App: React.FC = () => {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <Layout>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/threats" element={<ThreatDetection />} />
            <Route path="/analytics" element={<Analytics />} />
            <Route path="/settings" element={<div>Settings Page</div>} />
          </Routes>
        </Layout>
      </Router>
    </ThemeProvider>
  );
};

export default App;
