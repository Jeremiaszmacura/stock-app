import { useContext } from 'react';
import { Link, useNavigate } from 'react-router-dom';

import styles from './MainNavigation.module.css';
import { UserContext, AdminContext } from '../../UserContext';

const MainNavigation = () => {

    const { user, setUser } = useContext(UserContext);
    // eslint-disable-next-line no-unused-vars
    const { admin, setAdmin } = useContext(AdminContext);
    const navigate = useNavigate();

    const routeChange = () => {
        const path = '/';
        navigate(path);
      }

    const logOut = () => {
        fetch(
            'http://localhost:8000/auth/logout',
            {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                credentials: 'include'
            }
        ).then(res => {
            if (res.ok) {
                console.log('[CLIENT] logout - fetch successful');
            } else {
                console.log('[CLIENT] logout - fetch NOT successful');
            }
            res.json().then(data => console.log('[CLIENT] logout - ' + data.message));
        });
        localStorage.clear();
    };

    return (
        <header className={styles.header}>
            <div className={styles.logo} onClick={routeChange}>Stock App</div>
            <nav>
                <ul className={styles.nav_links}>
                    <li>
                        <Link className={styles.a} to='/'>Home</Link>
                    </li>
                    <li>
                        <Link className={styles.a} to='/VAR'>About VaR</Link>
                    </li>
            {user ? (
                <>
                <li>
                    <Link className={styles.a} to='/MyPortfolio'>My Portfolio</Link>
                </li>
                <li>
                    <Link className={styles.a} to='/dashboard'>Dashboard</Link>
                </li>
                <li>
                    <Link className={styles.a} to='/incandreq'>Inc & Req</Link>
                </li>
                <Link onClick={ () => {logOut(); setUser(null); setAdmin(null)} } to={'/'} ><button>Logout</button></Link>
                </>
            ) : (
                <>
                <li>
                    <Link className={styles.a} to='/register'>Register</Link>
                </li>
                <Link to='/login'><button>Login</button></Link>
                </>
            )}
                </ul>
            </nav>
        </header>
    )
}

export default MainNavigation;
