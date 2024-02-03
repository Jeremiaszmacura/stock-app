import { useNavigate } from 'react-router-dom';

import styles from './SearchResultUnit.module.css';

const SearchResultUnit = (props) => {

    const navigate = useNavigate();

    const selectHandler = (event) => {
        event.preventDefault();

        navigate('/company', { state: props });

    }

    return (
        <div className={styles.body}>
            <div onClick={selectHandler} className={styles.box}>
                <div className={styles.glass}></div>
                <div className={styles.content}>
                <p id={styles.symbol}>{props.symbol}</p>
                    <div className={styles.contentRow}>
                    </div>
                    <div className={styles.contentRow}>
                        <p>Name:</p>
                        <p>{props.name}</p>
                    </div>
                    <div className={styles.contentRow}>
                        <p>Type:</p>
                        <p>{props.type}</p>
                    </div>
                    <div className={styles.contentRow}>
                        <p>Region:</p>
                        <p>{props.region}</p>
                    </div>
                    <div className={styles.contentRow}>
                        <p>Market Open:</p>
                        <p>{props.marketOpen}</p>
                    </div>
                    <div className={styles.contentRow}>
                        <p>Market Close:</p>
                        <p>{props.marketClose}</p>
                    </div>
                    <div className={styles.contentRow}>
                        <p>Timezone:</p>
                        <p>{props.timezone}</p>
                    </div>
                    <div className={styles.contentRow}>
                        <p>Currency:</p>
                        <p>{props.currency}</p>
                    </div>
                    <div className={styles.contentRow}>
                        <p>Match Score:</p>
                        <p>{props.matchScore}</p>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default SearchResultUnit;
