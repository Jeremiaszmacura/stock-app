import { useRef } from 'react';

import styles from './LoginForm.module.css';

const RegisterForm = (props) => {

    const nameInputRef = useRef();
    const surnameInputRef = useRef();
    const emailInputRef = useRef();
    const passwordInputRef = useRef();
    const confirmPasswordInputRef = useRef();

    const submitHandler = (event) => {
        event.preventDefault();

        const enteredName = nameInputRef.current.value;
        const enteredSurname = surnameInputRef.current.value;
        const enteredEmail = emailInputRef.current.value;
        const enteredPassword = passwordInputRef.current.value;
        const enteredConfirmPassword = confirmPasswordInputRef.current.value;

        const registerData = {
            name: enteredName,
            surname:enteredSurname,
            email: enteredEmail,
            password: enteredPassword,
            confirm_password: enteredConfirmPassword,
        };

        props.onRegister(registerData);
    }

    return (
        <form className={styles.form} onSubmit={submitHandler}>
            <h1 className={styles.heading}>Register</h1>
            <div className={styles.control}>
                <label htmlFor='name'>Name</label>
                <input type='text' required id='name' ref={nameInputRef} />
            </div>
            <div className={styles.control}>
                <label htmlFor='name'>Surname</label>
                <input type='text' required id='surname' ref={surnameInputRef} />
            </div>
            <div className={styles.control}>
                <label htmlFor='email'>Email</label>
                <input type='text' required id='email' ref={emailInputRef} />
            </div>
            <div className={styles.control}>
                <label htmlFor='password'>Password</label>
                <input type='password' required id='password' ref={passwordInputRef} />
            </div>
            <div className={styles.control}>
                <label htmlFor='confirmPassword'>Repeat password</label>
                <input type='password' required id='confirm-password' ref={confirmPasswordInputRef} />
            </div>
            <div className={styles.actions}>
                <button>Register</button>
            </div>
        </form>
    );

}

export default RegisterForm;