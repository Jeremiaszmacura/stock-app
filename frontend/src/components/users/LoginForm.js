import { useRef } from 'react';

import styles from './LoginForm.module.css';

const LoginForm = (props) => {

    const emailInputRef = useRef();
    const passwordInputRef = useRef();

    const submitHandler = (event) => {
        event.preventDefault();

        const enteredEmail = emailInputRef.current.value;
        const enteredPassword = passwordInputRef.current.value;

        const loginData = {
            username: enteredEmail,
            password: enteredPassword,
        };

        props.onLogin(loginData);
    }

    return (
        <form className={styles.form} onSubmit={submitHandler}>
            <h1 className={styles.heading}>Log in</h1>
            <div className={styles.control}>
                <label htmlFor='email'>Email</label>
                <input type='text' required id='email' ref={emailInputRef} />
            </div>
            <div className={styles.control}>
                <label htmlFor='password'>Password</label>
                <input type='password' required id='password' ref={passwordInputRef} />
            </div>
            <div className={styles.actions}>
                <button>Login</button>
            </div>
        </form>
    );

}

export default LoginForm;
