import { useContext, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import jwt from 'jwt-decode'

import Card from '../components/ui/Card';
import LoginForm from "../components/users/LoginForm";
import { TokenContext, UserContext, AdminContext } from "../UserContext";
import styles from './Login.module.css'

const LoginPage = () => {

    const navigate = useNavigate();
    // eslint-disable-next-line no-unused-vars
    const {token, setToken} = useContext(TokenContext);
    // eslint-disable-next-line no-unused-vars
    const {user, setUser} = useContext(UserContext);
    // eslint-disable-next-line no-unused-vars
    const {admin, setAdmin} = useContext(AdminContext);

    const [loginError, setLoginError] = useState(null);

    const loginHandler = (loginData) => {
        fetch(
            'http://localhost:8000/auth/token',
            {
                method: 'POST',
                headers: {
                    'Accept': 'application/json'
                },
                body: new URLSearchParams(loginData),
                credentials: 'include'
            }
        )
        .then(res => {
            if (res.ok) {
                console.log('[CLIENT] login - fetch successful');
            } else {
                console.log('[CLIENT] login - fetch NOT successful');
            }
            res.json().then((data) => {
                if (data.access_token) {
                    const token = data.access_token;
                    const userData = jwt(token)
                    console.log(userData)
                    setToken(token);
                    setUser(userData);
                    if (userData.is_superuser === true) setAdmin(true);
                    localStorage.setItem('tokenInStorage', token);
                    localStorage.setItem('userInStorage', JSON.stringify(userData));
                    localStorage.setItem('roleInStorage', JSON.stringify(true));
                    navigate('/');
                } else {
                    setLoginError(data);
                    console.log(data)
                }
            });
        }).catch(err => {
            console.log(err);
        });
    };

    return (
        <section>
            <div className={styles.errorCard}>
                <Card>
                    <div className={styles.errorMessage}>
                        {loginError && <p>{loginError.error}</p>}
                    </div>
                    <LoginForm onLogin={loginHandler} />
                </Card>
            </div>

        </section>
    );
}

export default LoginPage;
