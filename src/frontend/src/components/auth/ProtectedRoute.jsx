import { Navigate, Outlet } from "react-router-dom";
import { useAuth } from "../../services/auth.jsx";

function ProtectedRoute({ allowedRoles }) {
  const { user } = useAuth();

  if (!user) return <Navigate to="/login" replace />;

  if (allowedRoles && !allowedRoles.includes(user.role)) {
    return <Navigate to={user.role === "admin" ? "/" : "/user"} replace />;
  }

  return <Outlet />;
}

export default ProtectedRoute;
