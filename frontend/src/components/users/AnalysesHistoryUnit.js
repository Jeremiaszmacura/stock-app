import { useNavigate } from 'react-router-dom';

import styles from './AnalysesHistoryUnit.module.css';

const AnalysesHistoryUnit = (props) => {

    const navigate = useNavigate();

    const selectHandler = (event) => {
        event.preventDefault();

        console.log("check this out!")

    }

    return (
        <div className={styles.historicalUnit}>
            <div onClick={selectHandler} className={styles.box}>
                <div className={styles.glass}></div>
                <div className={styles.content}>
                <p id={styles.symbol}>{props.symbol}</p>
                    <div className={styles.contentRow}>
                    </div>
                    <div className={styles.contentRow}>
                        <p>Name: "</p>
                        <p> {props.name}"</p>
                    </div>
                    <div className={styles.contentRow}>
                        <p>Region: "</p>
                        <p> {props.region}"</p>
                    </div>
                    <button id={styles.historyUnitDetailsButton}>
                        Details
                    </button>
                </div>
            </div>
        </div>
    );
}

export default AnalysesHistoryUnit;
