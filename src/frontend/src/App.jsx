import { BrowserRouter, Navigate, Outlet, Route, Routes } from "react-router-dom";
import { AuthProvider } from "./services/auth.jsx";
import ProtectedRoute from "./components/auth/ProtectedRoute";
import PublicRoute from "./components/auth/PublicRoute";
import Layout from "./components/layout/Layout";

import Dashboard from "./pages/Dashboard";
import Assets from "./pages/Assets";
import RiskAnalysis from "./pages/RiskAnalysis";
import Sensors from "./pages/Sensors";
import Weather from "./pages/Weather";
import Maintenance from "./pages/Maintenance";
import Crew from "./pages/Crew";
import AIAssistant from "./pages/AIAssistant";
import AssetDetails from "./pages/AssetDetails";
import ScrollToTop from "./components/layout/ScrollToTop";
import UserLayout from "./components/user/UserLayout";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import UserDashboard from "./pages/user/UserDashboard";
import MyService from "./pages/user/MyService";
import Outages from "./pages/user/Outages";
import Alerts from "./pages/user/Alerts";
import ReportIssue from "./pages/user/ReportIssue";
import CustomerAI from "./pages/user/CustomerAI";
import Profile from "./pages/user/Profile";

function AdminLayout() {
  return <Layout><Outlet /></Layout>;
}

function App() {
  return (
    <AuthProvider>
    <BrowserRouter>
      <ScrollToTop />

      <Routes>
        <Route element={<PublicRoute />}>
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<Signup />} />
        </Route>

        <Route element={<ProtectedRoute allowedRoles={["admin"]} />}>
          <Route element={<AdminLayout />}>
          <Route path="/" element={<Dashboard />} />
          <Route path="/assets" element={<Assets />} />
          <Route path="/assets/:assetId" element={<AssetDetails />} />
          <Route path="/risk" element={<RiskAnalysis />} />
          <Route path="/sensors" element={<Sensors />} />
          <Route path="/weather" element={<Weather />} />
          <Route path="/maintenance" element={<Maintenance />} />
          <Route path="/crew" element={<Crew />} />
          <Route path="/ai" element={<AIAssistant />} />
          </Route>
        </Route>

        <Route element={<ProtectedRoute allowedRoles={["user"]} />}>
          <Route element={<UserLayout />}>
            <Route path="/user" element={<UserDashboard />} />
            <Route path="/user/service" element={<MyService />} />
            <Route path="/user/outages" element={<Outages />} />
            <Route path="/user/alerts" element={<Alerts />} />
            <Route path="/user/report" element={<ReportIssue />} />
            <Route path="/user/ai" element={<CustomerAI />} />
            <Route path="/user/profile" element={<Profile />} />
          </Route>
        </Route>

        <Route path="*" element={<Navigate to="/login" replace />} />
      </Routes>
    </BrowserRouter>
    </AuthProvider>
  );
}

export default App;
