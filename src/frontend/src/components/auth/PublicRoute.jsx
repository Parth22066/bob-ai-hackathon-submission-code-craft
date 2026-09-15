import { Navigate, Outlet } from "react-router-dom";
import { useAuth } from "../../services/auth.jsx";

function PublicRoute() {
  const { user } = useAuth();

  if (user) return <Navigate to={user.role === "admin" ? "/" : "/user"} replace />;

  return <Outlet />;
}

export default PublicRoute;
