import { useState, useMemo, useEffect } from 'react';
import { Route, Routes } from 'react-router-dom';

import HomePage from './pages/Home';
import VARPage from './pages/VAR';
import CompanyPage from './pages/Company';
import MyPortfolioPage from './pages/MyPortfolio';
import DashboardPage from './pages/Dashboard';
import LoginPage from './pages/Login';
import RegisterPage from './pages/Register';
import IncAndReqPage from './pages/IncAndReq';
import Layout from './components/layout/Layout';
import { TokenContext, UserContext, AdminContext } from './UserContext';

const App = () => {

  const [token, setToken] = useState(null);
  const [user, setUser] = useState(null);
  const [admin, setAdmin] = useState(null);

  const value0 = useMemo(() => ({ token, setToken }), [token, setToken])
  const value = useMemo(() => ({ user, setUser }), [user, setUser]);
  const value2 = useMemo(() => ({ admin, setAdmin }), [admin, setAdmin]);

  useEffect(() => {
    const tokenInStorage = localStorage.getItem("tokenInStorage");
    const userFromStorage = localStorage.getItem("userInStorage");
    const roleFromStorage = localStorage.getItem("roleInStorage");
    if (tokenInStorage) {
      const tokenInStorageParsed = JSON.stringify(tokenInStorage)
      setUser(tokenInStorageParsed);
  }
    if (userFromStorage) {
        const userFromStorageParsed = JSON.stringify(userFromStorage)
        setUser(userFromStorageParsed);
    }
    if (roleFromStorage) {
        const roleFromStorageParsed = JSON.stringify(roleFromStorage)
        setAdmin(roleFromStorageParsed);
    }
  }, []);

  return (
    <TokenContext.Provider value={value0}>
      <UserContext.Provider value={value}>
        <AdminContext.Provider value={value2}>
          <Layout>
            <Routes>
              <Route path='/' exact element={<HomePage />}>
              </Route>
              <Route path='/VAR' exact element={<VARPage />}>
              </Route>
              <Route path='/company' exact element={<CompanyPage />}>
              </Route>
              <Route path='/MyPortfolio' exact element={<MyPortfolioPage />}>
              </Route>
              <Route path='/dashboard' exact element={<DashboardPage />}>
              </Route>
              <Route path='/incandreq' exact element={<IncAndReqPage />}>
              </Route>
              <Route path='/register' exact element={<RegisterPage />}>
              </Route>
              <Route path='/login' exact element={<LoginPage />}>
              </Route>
            </Routes>
          </Layout>
        </AdminContext.Provider>
      </UserContext.Provider>
    </TokenContext.Provider>
  );
}

export default App;
