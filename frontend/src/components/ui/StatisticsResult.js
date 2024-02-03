import styles from './StatisticsResult.module.css';

const StatisticsResult = (props) => {
    return (
        <div className={styles.body}>
            <div className={styles.box}>
                <div className={styles.glass}></div>
                <div className={styles.content}>
                    {props.children}
                </div>
            </div>
        </div>
    );
}

export default StatisticsResult;
