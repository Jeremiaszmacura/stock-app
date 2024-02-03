import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

import Card from '../components/ui/Card';
import LoginForm from "../components/users/RegisterForm";
import styles from './Login.module.css'

const LoginPage = () => {

    const navigate = useNavigate();
    const [registerError, setRegisterError] = useState(null);

    const registerHandler = (registerData) => {
        fetch(
            'http://localhost:8000/users/',
            {
                method: 'POST',
                body: JSON.stringify(registerData),
                headers: {
                    'Content-Type': 'application/json'
                }
            }
        ).then(res => {
            if (res.ok) {
                console.log('[CLIENT] register - fetch successful');
            } else {
                console.log('[CLIENT] register - fetch NOT successful');
            }
            res.json().then((data) => {
                if (data.email === registerData.email) {
                    console.log('[CLIENT] registered successfuly - ' + data);
                    navigate('/login');
                } else {
                    setRegisterError(data);
                    console.log(data)
                }
            });
        });
    };

    return (
        <section>
            <div className={styles.errorCard}>
                <Card>
                    <div className={styles.errorMessage}>
                        {registerError && <p>{registerError.error}</p>}
                    </div>
                    <LoginForm onRegister={registerHandler} />
                </Card>
            </div>

        </section>
    );
}

export default LoginPage;
